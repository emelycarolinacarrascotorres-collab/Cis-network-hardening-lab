#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cis_hardening.py - Auditoría y hardening automatizado (CIS Cisco IOS Benchmark)

Modos (--mode):
  audit       Solo escanea y genera informe. NO modifica ningún equipo (por defecto).
  remediate   Respalda, aplica las reglas que fallan, re-escanea y genera informe
              póstumo (antes / después).

Equipos soportados: Cisco IOS (router/switch) y FortiGate (FortiOS, rol "firewall").

Origen de los equipos:
  --inventory inventory.json          Conexión SSH real (requiere: pip install netmiko)
  --offline R1.cfg:router SW1.cfg:switch   Trabaja sobre archivos 'show running-config'
                                       (simulación; útil para probar sin el laboratorio)

Ejemplos:
  python3 cis_hardening.py --mode audit
  python3 cis_hardening.py --mode remediate --yes
  python3 cis_hardening.py --offline lab_configs/R1-baseline.cfg:router --mode remediate
  python3 cis_hardening.py --list-controls

Variables de entorno (evitan los prompts):
  CIS_USER, CIS_PASS, CIS_ENABLE   credenciales SSH y enable actual (Cisco)
  FGT_USER, FGT_PASS               credenciales del FortiGate (rol "firewall")
  CIS_ENABLE_NEW                   nuevo 'enable secret' (si no existe, MGT-03 queda MANUAL)
"""
from __future__ import annotations

import argparse
import datetime as dt
import getpass
import html
import json
import os
import re
import shlex
import sys
from pathlib import Path

PASS, FAIL, MANUAL, NA = "PASS", "FAIL", "MANUAL", "N/A"
BENCHMARK = "CIS Benchmarks: Cisco IOS y FortiGate (selección de controles)"
VTY_ACL = "CIS-VTY-ACL"
SECRET_TOKEN = "{{ENABLE_SECRET}}"

DEFAULT_PARAMS = {
    "mgmt_network": "10.25.20.0 0.0.0.255",   # red desde la que se permite administrar (VLAN 99)
    "syslog_server": "10.25.20.10",           # PC-Admin con rsyslog
    "fw_trusthost": "10.25.20.0 255.255.255.0",   # FortiGate: red desde la que se permite administrar
    "fw_hostname": "FW1",                          # FortiGate: nombre a asignar si está por defecto
    "banner": ("AUTHORIZED ACCESS ONLY. Activity is monitored and logged. "
               "Disconnect immediately if you are not an authorized user."),
}

# ----------------------------------------------------------------------------
# Modelo mínimo de configuración IOS (para auditar y simular cambios offline)
# ----------------------------------------------------------------------------
KEY_PREFIXES = (
    "exec-timeout", "transport input", "access-class", "logging host",
    "logging buffered", "banner login", "banner motd", "ip ssh version",
    "ip ssh time-out", "ip ssh authentication-retries", "hostname",
    "service timestamps debug", "service timestamps log",
)


def keyof(line: str) -> str:
    """Clave de 'misma directiva' para reemplazar valores al simular cambios."""
    if re.match(r"enable (algorithm-type \w+ )?(secret|password)\b", line):
        return "enable-secret"
    for p in KEY_PREFIXES:
        if line.startswith(p):
            return p
    t = line.split()
    return " ".join(t[:-1]) if len(t) > 2 else line


class Config:
    def __init__(self, text: str):
        self.items: dict[str, list[str]] = {}   # cabecera/línea global -> hijos
        header = None
        lines = iter(text.splitlines())
        for raw in lines:
            line = raw.rstrip()
            if not line.strip() or line.startswith("!"):
                header = None
                continue
            if line[0] in " \t":
                if header is not None:
                    self.items[header].append(line.strip())
                continue
            if line.startswith(("Building configuration", "Current configuration", "Using ")) or line == "end":
                header = None
                continue
            m = re.match(r"banner (\w+) (.*)", line)
            if m:  # banner multilínea: consumir hasta el delimitador
                rest = m.group(2)
                delim = "^C" if rest.startswith("^C") else ("\x03" if rest.startswith("\x03") else rest[:1])
                if delim and delim not in rest[len(delim):]:
                    for nxt in lines:
                        if delim in nxt:
                            break
                self.items.setdefault(f"banner {m.group(1)}", [])
                header = None
                continue
            header = line
            self.items.setdefault(line, [])

    # -- consultas -----------------------------------------------------------
    def has(self, pattern: str) -> bool:
        return any(re.search(pattern, k) for k in self.items)

    def blocks(self, pattern: str):
        return [(h, c) for h, c in self.items.items() if re.search(pattern, h)]

    # -- simulación de cambios (solo modo offline) ----------------------------
    def apply(self, cmds: list[str]) -> None:
        hdr = None
        for i, c in enumerate(cmds):
            if c.startswith(" "):
                if hdr is not None:
                    self._child(hdr, c.strip())
            else:
                nxt = cmds[i + 1] if i + 1 < len(cmds) else ""
                if nxt.startswith(" "):
                    hdr = c
                    self.items.setdefault(c, [])
                else:
                    hdr = None
                    self._global(c)

    def _global(self, line: str) -> None:
        if line.startswith("no "):
            pos = line[3:]
            for k in [k for k in self.items if k == pos or k.startswith(pos + " ")]:
                if not self.items[k]:
                    del self.items[k]
            self.items.setdefault(line, [])
        else:
            key = keyof(line)
            for k in [k for k in self.items
                      if not self.items[k] and k != line and (keyof(k) == key or k == "no " + line)]:
                del self.items[k]
            self.items.setdefault(line, [])

    def _child(self, hdr: str, line: str) -> None:
        ch = self.items.setdefault(hdr, [])
        if line.startswith("no "):
            pos = line[3:]
            ch[:] = [c for c in ch if not (c == pos or c.startswith(pos + " "))]
        else:
            key = keyof(line)
            ch[:] = [c for c in ch if c == line or (keyof(c) != key and c != "no " + line)]
        if line not in ch:
            ch.append(line)

    def to_text(self) -> str:
        out = []
        for h, ch in self.items.items():
            out.append(h)
            out += [" " + c for c in ch]
            out.append("!")
        return "\n".join(out) + "\nend\n"


# ----------------------------------------------------------------------------
# Definición de controles: cada uno tiene check() y fix()
# ----------------------------------------------------------------------------
def sub(s: str, p: dict) -> str:
    return (s.replace("{mgmt}", p["mgmt_network"]).replace("{syslog}", p["syslog_server"])
             .replace("{banner}", p["banner"]).replace("{acl}", VTY_ACL)
             .replace("{fw_hostname}", p["fw_hostname"]).replace("{fw_trusthost}", p["fw_trusthost"]))


def present(want=None, forbid=None, fix=(), msg="No cumple"):
    def check(cfg, p):
        ok = (want is None or cfg.has(want)) and (forbid is None or not cfg.has(forbid))
        return (PASS, "") if ok else (FAIL, msg)
    return check, (lambda cfg, p: [sub(f, p) for f in fix])


def numeric(pattern, ok_fn, fixline, msg):
    def check(cfg, p):
        for k in cfg.items:
            m = re.fullmatch(pattern, k)
            if m:
                v = int(m.group(1))
                return (PASS, "") if ok_fn(v) else (FAIL, f"{msg} (actual: {v})")
        return FAIL, f"{msg} (no configurado)"
    return check, (lambda cfg, p: [fixline])


def per_block(header_re, ok, children, applies=lambda c: True, pre=lambda p: []):
    def sel(cfg):
        return [(h, c) for h, c in cfg.blocks(header_re) if applies(c)]

    def check(cfg, p):
        s = sel(cfg)
        if not s:
            return NA, "sin elementos aplicables"
        bad = [h for h, c in s if not ok(c)]
        return (FAIL, "No cumple: " + "; ".join(bad)) if bad else (PASS, "")

    def fix(cfg, p):
        bad = [h for h, c in sel(cfg) if not ok(c)]
        if not bad:
            return []
        cmds = list(pre(p))
        for h in bad:
            cmds += [h] + [" " + sub(x, p) for x in children]
        return cmds
    return check, fix


def timeout_ok(ch):
    for c in ch:
        m = re.fullmatch(r"exec-timeout (\d+)(?: (\d+))?", c)
        if m:
            total = int(m.group(1)) * 60 + int(m.group(2) or 0)
            return 0 < total <= 600
    return False


def chk_users(cfg, p):
    bad = [k.split()[1] for k in cfg.items if re.match(r"username \S+ .*\b(password|nopassword)\b", k)]
    return (FAIL, "Usuarios sin 'secret': " + ", ".join(bad)) if bad else (PASS, "")


def chk_enable(cfg, p):
    if cfg.has(r"^enable password"):
        return FAIL, "Existe 'enable password' (reversible / texto claro)"
    if cfg.has(r"^enable (secret|algorithm-type \w+ secret)"):
        return PASS, ""
    return FAIL, "No hay 'enable secret'"


def fix_enable(cfg, p):
    if p.get("new_enable_secret"):
        return ["no enable password", f"enable algorithm-type scrypt secret {SECRET_TOKEN}"]
    return []


def chk_snmp(cfg, p):
    bad = [k for k in cfg.items if re.match(r"snmp-server community (public|private)\b", k)]
    return (FAIL, "Communities por defecto: " + ", ".join(k.split()[2] for k in bad)) if bad else (PASS, "")


def fix_snmp(cfg, p):
    return ["no " + " ".join(k.split()[:3]) for k in cfg.items
            if re.match(r"snmp-server community (public|private)\b", k)]


def chk_ts(cfg, p):
    miss = [w for w in ("debug", "log") if not cfg.has(rf"^service timestamps {w} datetime")]
    return (FAIL, "Falta timestamps: " + ", ".join(miss)) if miss else (PASS, "")


def fix_ts(cfg, p):
    return [f"service timestamps {w} datetime msec" for w in ("debug", "log")
            if not cfg.has(rf"^service timestamps {w} datetime")]


class Control:
    def __init__(self, id, title, ref, why, check, fix, roles):
        self.id, self.title, self.ref, self.why = id, title, ref, why
        self.check, self.fix, self.roles = check, fix, roles


CONTROLS: list[Control] = []


def add(id, title, ref, why, cf, roles=("router", "switch")):
    CONTROLS.append(Control(id, title, ref, why, cf[0], cf[1], roles))


# --- Management plane --------------------------------------------------------
add("MGT-01", "Habilitar 'aaa new-model'", "1.1.1",
    "Activa AAA: base para autenticación por listas de métodos y trazabilidad de accesos.",
    present(want=r"^aaa new-model$", fix=["aaa new-model"]))
add("MGT-02", "Definir 'aaa authentication login default'", "1.1.2",
    "Obliga a que consola y VTY usen un método de autenticación explícito (local) en vez de contraseñas de línea.",
    present(want=r"^aaa authentication login default ", fix=["aaa authentication login default local"]))
add("MGT-03", "Usar 'enable secret' (sin 'enable password')", "1.4.1",
    "El modo privilegiado debe protegerse con hash fuerte (scrypt) y no con una contraseña reversible.",
    (chk_enable, fix_enable))
add("MGT-04", "Habilitar 'service password-encryption'", "1.4.2",
    "Evita que contraseñas de línea aparezcan en texto claro al ver la configuración (mitigación básica).",
    present(want=r"^service password-encryption$", fix=["service password-encryption"]))
add("MGT-05", "Usuarios locales con 'secret' (no 'password')", "1.4.3",
    "Un hash fuerte protege las credenciales locales si se filtra la configuración. Requiere acción manual (no se conoce la clave).",
    (chk_users, lambda cfg, p: []))
add("MGT-06", "exec-timeout <= 10 min en consola", "1.2.7",
    "Cierra sesiones de consola abandonadas; reduce el riesgo de acceso físico oportunista.",
    per_block(r"^line con 0$", timeout_ok, ["exec-timeout 10 0"]))
add("MGT-07", "exec-timeout <= 10 min en VTY", "1.2.8",
    "Cierra sesiones remotas inactivas; reduce la ventana para secuestro de sesión.",
    per_block(r"^line vty ", timeout_ok, ["exec-timeout 10 0"]))
add("MGT-08", "'transport input ssh' en VTY", "1.2.2",
    "Telnet envía credenciales en claro; solo se permite SSH (cifrado).",
    per_block(r"^line vty ", lambda c: "transport input ssh" in c, ["transport input ssh"]))
add("MGT-09", "ACL de acceso (access-class) en VTY", "1.2.4 / 1.2.5",
    "Solo la red de gestión puede intentar conectarse por SSH al dispositivo (reduce superficie de ataque).",
    per_block(r"^line vty ", lambda c: any(x.startswith("access-class ") for x in c), ["access-class {acl} in"],
              pre=lambda p: [f"ip access-list standard {VTY_ACL}", " permit " + p["mgmt_network"], " deny any log"]))
add("MGT-10", "Configurar 'banner login'", "1.3.2",
    "Aviso legal de acceso autorizado: base legal para sancionar accesos no autorizados.",
    present(want=r"^banner login", fix=["banner login #{banner}#"]))
add("MGT-11", "Eliminar SNMP communities 'public'/'private'", "1.5.2 / 1.5.3",
    "Son las primeras cadenas que prueba cualquier atacante; 'private' (RW) permite modificar el equipo.",
    (chk_snmp, fix_snmp))
add("MGT-12", "Deshabilitar servidor HTTP ('no ip http server')", "2.1.x",
    "HTTP es texto claro y expande la superficie de ataque; la gestión se hace por SSH.",
    present(forbid=r"^ip http server$", fix=["no ip http server"], msg="'ip http server' activo"))
add("MGT-13", "SSH versión 2", "2.1.1.x",
    "SSHv1 tiene debilidades criptográficas conocidas.",
    present(want=r"^ip ssh version 2$", fix=["ip ssh version 2"]))
add("MGT-14", "'ip ssh time-out' <= 60 s", "2.1.1.2",
    "Limita el tiempo para completar la autenticación SSH (mitiga conexiones colgadas / DoS).",
    numeric(r"ip ssh time-out (\d+)", lambda v: 0 < v <= 60, "ip ssh time-out 60", "Debe ser <= 60"))
add("MGT-15", "'ip ssh authentication-retries' <= 3", "2.1.1.3",
    "Limita intentos de contraseña por sesión SSH (mitiga fuerza bruta).",
    numeric(r"ip ssh authentication-retries (\d+)", lambda v: 0 < v <= 3,
            "ip ssh authentication-retries 3", "Debe ser <= 3"))
# --- Control plane ----------------------------------------------------------
add("CTL-01", "Deshabilitar CDP ('no cdp run')", "2.1.2",
    "CDP revela modelo, IOS e IPs a cualquier vecino L2 (reconocimiento).",
    present(want=r"^no cdp run$", fix=["no cdp run"]))
add("CTL-02", "'no ip bootp server'", "2.1.3",
    "Servicio innecesario que expone el equipo a abuso/descarga de configuración.",
    present(want=r"^no ip bootp server$", fix=["no ip bootp server"]))
add("CTL-03", "'no service pad'", "2.1.8",
    "PAD (X.25) es un servicio heredado y sin uso; se elimina para reducir superficie.",
    present(want=r"^no service pad$", fix=["no service pad"]))
add("CTL-04", "'logging buffered' >= 16384", "2.2.2",
    "Un buffer mayor conserva eventos para análisis forense local.",
    numeric(r"logging buffered (\d+)", lambda v: v >= 16384, "logging buffered 64000", "Debe ser >= 16384"))
add("CTL-05", "Enviar logs a servidor syslog", "2.2.4",
    "Logs centralizados no se pierden si el equipo se reinicia o es comprometido.",
    present(want=r"^logging (host )?\d+\.\d+\.\d+\.\d+", fix=["logging host {syslog}"]))
add("CTL-06", "Timestamps con fecha/hora en logs y debug", "2.2.6",
    "Sin marca de tiempo no se pueden correlacionar eventos durante un incidente.",
    (chk_ts, fix_ts))
# --- Data plane -------------------------------------------------------------
add("DAT-01", "'no ip source-route'", "3.1.1",
    "Impide que el origen dicte la ruta del paquete (técnica usada para evadir controles).",
    present(want=r"^no ip source-route$", fix=["no ip source-route"]), roles=("router",))
add("DAT-02", "'no ip proxy-arp' en interfaces L3", "3.1.x",
    "Evita que el router responda ARP por otros hosts (suplantación / fuga entre segmentos).",
    per_block(r"^interface ", lambda c: "no ip proxy-arp" in c, ["no ip proxy-arp"],
              applies=lambda c: any(x.startswith("ip address ") for x in c)))
# --- Capa 2 (buenas prácticas; no numeradas en CIS IOS) ---------------------
add("L2-01", "BPDU Guard por defecto en puertos PortFast", "L2 (extra)",
    "Un puerto de acceso que reciba BPDUs (switch rogue) se bloquea, protegiendo la raíz STP.",
    present(want=r"^spanning-tree portfast bpduguard default$",
            fix=["spanning-tree portfast bpduguard default"]), roles=("switch",))
add("L2-02", "Port-security en puertos de acceso", "L2 (extra)",
    "Limita la cantidad de MAC por puerto (mitiga MAC flooding y conexión de equipos no autorizados).",
    per_block(r"^interface (Fast|Gigabit|TenGigabit)Ethernet", lambda c: any(x.startswith("switchport port-security") for x in c),
              ["switchport port-security", "switchport port-security maximum 2",
               "switchport port-security violation restrict", "switchport port-security mac-address sticky"],
              applies=lambda c: "switchport mode access" in c), roles=("switch",))

# ----------------------------------------------------------------------------
# FortiGate (FortiOS): parser y controles basados en el CIS FortiGate Benchmark
# ----------------------------------------------------------------------------
class FGConfig:
    """Parser mínimo de 'show full-configuration' de FortiOS (config/edit/set/next/end)."""

    def __init__(self, text: str = ""):
        self.sections: dict[tuple, dict[str, list[str]]] = {}
        self.raw, self.extra, self._stack = text, [], []
        self.feed(text.splitlines())

    def feed(self, lines) -> None:
        self._stack = []
        for raw in lines:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                tok = shlex.split(line)
            except ValueError:
                tok = line.split()
            kw, st = tok[0], self._stack
            if kw == "config":
                st.append(" ".join(tok[1:]))
                self.sections.setdefault(tuple(st), {})
            elif kw == "edit":
                st.append(tok[1] if len(tok) > 1 else "")
                self.sections.setdefault(tuple(st), {})
            elif kw == "next":
                if len(st) > 1:
                    st.pop()
            elif kw == "end":
                if st:
                    st.pop()
            elif kw == "set" and st and len(tok) > 1:
                self.sections.setdefault(tuple(st), {})[tok[1]] = tok[2:]
            elif kw == "append" and st and len(tok) > 1:
                self.sections.setdefault(tuple(st), {}).setdefault(tok[1], []).extend(tok[2:])
            elif kw == "unset" and st and len(tok) > 1:
                self.sections.setdefault(tuple(st), {}).pop(tok[1], None)

    def settings(self, path: str):
        return self.sections.get((path,))

    def entries(self, path: str):
        return [(k[1], v) for k, v in self.sections.items() if len(k) == 2 and k[0] == path]

    # simulación offline: se anexan los comandos y se re-interpretan
    def apply(self, cmds: list[str]) -> None:
        self.extra += cmds
        self.feed(cmds)

    def to_text(self) -> str:
        return self.raw.rstrip() + "\n\n# --- Remediación CIS (script) ---\n" + "\n".join(self.extra) + "\n"


def parse_config(text: str, role: str):
    return FGConfig(text) if role == "firewall" else Config(text)


def _int(v) -> int:
    try:
        return int(v[0])
    except (ValueError, IndexError, TypeError):
        return -1


def fg_set(path, key, ok, msg, fixlines):
    def check(cfg, p):
        s = cfg.settings(path)
        if s is None:
            return NA, f"sección '{path}' no encontrada"
        if key not in s:
            return FAIL, f"'{key}' no visible (use 'show full-configuration')"
        return (PASS, "") if ok(s[key]) else (FAIL, f"{msg} (actual: {' '.join(s[key])})")
    return check, (lambda cfg, p: [f"config {path}"] + [sub(f, p) for f in fixlines] + ["end"])


def fg_entries(path, bad, fixfn):
    def q(n):
        return n if n.isdigit() else f'"{n}"'

    def check(cfg, p):
        ents = cfg.entries(path)
        if not ents:
            return NA, f"sin entradas en '{path}'"
        b = [n for n, s in ents if bad(s)]
        return (FAIL, "No cumple: " + ", ".join(b)) if b else (PASS, "")

    def fix(cfg, p):
        body = []
        for n, s in cfg.entries(path):
            if bad(s):
                f = fixfn(n, s, p)
                if f:
                    body += [f"edit {q(n)}"] + f + ["next"]
        return [f"config {path}"] + body + ["end"] if body else []
    return check, fix


def chk_fg_pwpol(cfg, p):
    s = cfg.settings("system password-policy")
    if s is None:
        return FAIL, "política de contraseñas no encontrada"
    cls = ("min-lower-case-letter", "min-upper-case-letter", "min-number", "min-non-alphanumeric")
    ok = (s.get("status") == ["enable"] and _int(s.get("minimum-length")) >= 8
          and all(_int(s.get(k)) >= 1 for k in cls))
    return (PASS, "") if ok else (FAIL, "Política deshabilitada, longitud < 8 o sin complejidad")


def chk_fg_syslog(cfg, p):
    s = cfg.settings("log syslogd setting")
    if s is None:
        return FAIL, "syslogd no encontrado"
    ok = s.get("status") == ["enable"] and bool(s.get("server")) and s["server"] != [""]
    return (PASS, "") if ok else (FAIL, "Syslog remoto deshabilitado o sin servidor")


def chk_fg_autoinstall(cfg, p):
    s = cfg.settings("system auto-install")
    if s is None:
        return NA, "no aplica (sin auto-install en este equipo)"
    ok = s.get("auto-install-config") == ["disable"] and s.get("auto-install-image") == ["disable"]
    return (PASS, "") if ok else (FAIL, "Auto-instalación por USB habilitada")


def fg_anyany(s) -> bool:
    return (s.get("action") == ["accept"] and s.get("srcaddr") == ["all"] and s.get("dstaddr") == ["all"]
            and s.get("service") == ["ALL"] and s.get("status", ["enable"]) != ["disable"])


def fix_fg_if(n, s, p):
    rem = [t for t in s.get("allowaccess", []) if t not in ("telnet", "http")]
    return [f"set allowaccess {' '.join(rem)}"] if rem else ["unset allowaccess"]


FW = ("firewall",)
add("FGT-01", "Hostname distinto al valor por defecto", "FortiGate · Sistema",
    "Un nombre propio facilita inventario y correlación de logs; el nombre por defecto delata el modelo.",
    fg_set("system global", "hostname", lambda v: bool(v) and not v[0].lower().startswith("fortigate"),
           "Hostname por defecto", ["set hostname {fw_hostname}"]), roles=FW)
add("FGT-02", "Banner previo al login habilitado", "FortiGate · Sistema",
    "Aviso legal de acceso autorizado antes de autenticarse.",
    fg_set("system global", "pre-login-banner", lambda v: v == ["enable"], "Banner deshabilitado",
           ["set pre-login-banner enable"]), roles=FW)
add("FGT-03", "Timeout de inactividad de administración <= 5 min", "FortiGate · Sistema",
    "Cierra sesiones de administración abandonadas.",
    fg_set("system global", "admintimeout", lambda v: 0 < _int(v) <= 5, "Debe ser <= 5 minutos",
           ["set admintimeout 5"]), roles=FW)
add("FGT-04", "Strong-crypto habilitado", "FortiGate · Sistema",
    "Fuerza protocolos y cifrados robustos (TLS/SSH) en la administración.",
    fg_set("system global", "strong-crypto", lambda v: v == ["enable"], "Strong-crypto deshabilitado",
           ["set strong-crypto enable"]), roles=FW)
add("FGT-05", "Bloqueo de admin: umbral <= 3 intentos", "FortiGate · Sistema",
    "Mitiga fuerza bruta contra las cuentas de administración.",
    fg_set("system global", "admin-lockout-threshold", lambda v: 1 <= _int(v) <= 3, "Debe estar entre 1 y 3",
           ["set admin-lockout-threshold 3"]), roles=FW)
add("FGT-06", "Bloqueo de admin: duración >= 900 s", "FortiGate · Sistema",
    "Un bloqueo suficientemente largo frena los ataques de adivinación de contraseñas.",
    fg_set("system global", "admin-lockout-duration", lambda v: _int(v) >= 900, "Debe ser >= 900 s",
           ["set admin-lockout-duration 900"]), roles=FW)
add("FGT-07", "Administradores con 'trusthost' restringido", "FortiGate · Sistema",
    "Cada cuenta admin solo debe poder iniciar sesión desde la red de gestión (evita 0.0.0.0/0).",
    fg_entries("system admin",
               lambda s: not s.get("trusthost1") or s["trusthost1"][:2] == ["0.0.0.0", "0.0.0.0"],
               lambda n, s, p: [f"set trusthost1 {p['fw_trusthost']}"]), roles=FW)
add("FGT-08", "Sin Telnet ni HTTP en 'allowaccess' de interfaces", "FortiGate · Red",
    "Telnet y HTTP viajan en claro; la administración debe ser solo por HTTPS/SSH.",
    fg_entries("system interface",
               lambda s: any(t in ("telnet", "http") for t in s.get("allowaccess", [])), fix_fg_if), roles=FW)
add("FGT-09", "Política de contraseñas habilitada (longitud y complejidad)", "FortiGate · Sistema",
    "Contraseñas largas y complejas reducen el éxito de ataques de diccionario.",
    (chk_fg_pwpol, lambda cfg, p: ["config system password-policy", "set status enable",
     "set minimum-length 12", "set min-lower-case-letter 1", "set min-upper-case-letter 1",
     "set min-number 1", "set min-non-alphanumeric 1", "end"]), roles=FW)
add("FGT-10", "Agente SNMP deshabilitado", "FortiGate · Sistema",
    "Si no se usa, el agente SNMP solo agrega superficie de ataque (y v1/v2c no cifra).",
    fg_set("system snmp sysinfo", "status", lambda v: v == ["disable"], "SNMP habilitado",
           ["set status disable"]), roles=FW)
add("FGT-11", "Logs enviados a servidor syslog", "FortiGate · Logging",
    "Logs centralizados no se pierden si el equipo se compromete o reinicia.",
    (chk_fg_syslog, lambda cfg, p: ["config log syslogd setting", "set status enable",
     f'set server "{p["syslog_server"]}"', "end"]), roles=FW)
add("FGT-12", "Sincronización NTP habilitada", "FortiGate · Sistema",
    "Hora correcta es indispensable para correlacionar eventos.",
    fg_set("system ntp", "ntpsync", lambda v: v == ["enable"], "NTP deshabilitado",
           ["set ntpsync enable"]), roles=FW)
add("FGT-13", "Logging de tráfico en todas las políticas", "FortiGate · Políticas",
    "Sin 'logtraffic all' no hay registro del tráfico permitido para análisis forense.",
    fg_entries("firewall policy", lambda s: s.get("logtraffic") != ["all"],
               lambda n, s, p: ["set logtraffic all"]), roles=FW)
add("FGT-14", "Sin políticas ANY-ANY-ALL con 'accept'", "FortiGate · Políticas",
    "Una política que permite todo origen, destino y servicio anula el firewall. Requiere diseño manual (qué sí se permite).",
    fg_entries("firewall policy", fg_anyany, lambda n, s, p: []), roles=FW)
add("FGT-15", "Auto-instalación por USB deshabilitada", "FortiGate · Sistema",
    "Evita que alguien con acceso físico cargue configuración o firmware desde un USB.",
    (chk_fg_autoinstall, lambda cfg, p: ["config system auto-install", "set auto-install-config disable",
     "set auto-install-image disable", "end"]), roles=FW)


# ----------------------------------------------------------------------------
# Motor de auditoría / remediación
# ----------------------------------------------------------------------------
def run_audit(cfg: Config, role: str, params: dict, only=None) -> list[dict]:
    res = []
    for c in CONTROLS:
        if only and c.id not in only:
            continue
        if not (role in c.roles or (role == "both" and ("router" in c.roles or "switch" in c.roles))):
            continue
        try:
            st, det = c.check(cfg, params)
            fx = c.fix(cfg, params) if st == FAIL else []
        except Exception as e:  # un control roto no debe tumbar el escaneo
            st, det, fx = MANUAL, f"error evaluando control: {e}", []
        if st == FAIL and not fx:
            st = MANUAL
            det = (det + " -> requiere acción manual").strip()
        res.append({"id": c.id, "title": c.title, "ref": c.ref, "why": c.why,
                    "status": st, "detail": det, "fix": fx})
    return res


def score(res: list[dict]) -> float:
    c = [r for r in res if r["status"] != NA]
    return round(100 * sum(r["status"] == PASS for r in c) / len(c), 1) if c else 100.0


def to_cli(cmds: list[str]) -> list[str]:
    out, in_blk = [], False
    for i, c in enumerate(cmds):
        if c.startswith(" "):
            out.append(c.strip())
            continue
        if in_blk:
            out.append("exit")
        in_blk = i + 1 < len(cmds) and cmds[i + 1].startswith(" ")
        out.append(c.strip())
    return out


def push(conn, cmds: list[str]) -> list[str]:
    secret = os.environ.get("CIS_ENABLE_NEW", "")
    cli = [c.replace(SECRET_TOKEN, secret) for c in to_cli(cmds)]
    out = conn.send_config_set(cli, cmd_verify=False, read_timeout=120)
    bad = ("fail", "unknown action", "parse error", "invalid", "error")
    errs = [l.strip() for l in out.splitlines()
            if l.strip().startswith("%") or any(b in l.lower() for b in bad)]
    return [e.replace(secret, "***") if secret else e for e in errs]


def connect(dev: dict, creds: tuple):
    try:
        from netmiko import ConnectHandler
    except ImportError:
        sys.exit("Falta netmiko. Instale con: pip install netmiko  (o use --offline)")
    user, pw, en = creds
    conn = ConnectHandler(device_type=dev.get("device_type", "cisco_ios"), host=dev["host"],
                          username=user, password=pw, secret=en, timeout=30)
    if en and dev.get("role") != "firewall":
        conn.enable()
    return conn


_CREDS: dict = {}


def get_creds(prefix: str, ask_enable: bool) -> tuple:
    if prefix not in _CREDS:
        user = os.environ.get(f"{prefix}_USER") or input(f"[{prefix}] Usuario: ")
        pw = os.environ.get(f"{prefix}_PASS") or getpass.getpass(f"[{prefix}] Password: ")
        en = ""
        if ask_enable:
            en = os.environ.get(f"{prefix}_ENABLE") or getpass.getpass(f"[{prefix}] Enable actual (Enter si no aplica): ")
        _CREDS[prefix] = (user, pw, en)
    return _CREDS[prefix]


# ----------------------------------------------------------------------------
# Reportes
# ----------------------------------------------------------------------------
ICON = {PASS: "[ OK ]", FAIL: "[FAIL]", MANUAL: "[MANU]", NA: "[ -- ]"}


def print_results(title: str, res: list[dict]) -> None:
    print(f"\n  {title} - cumplimiento: {score(res)}%")
    for r in res:
        extra = f"  <- {r['detail']}" if r["detail"] else ""
        print(f"   {ICON[r['status']]} {r['id']}  {r['title']}{extra}")


def html_report(rep: dict) -> str:
    e = html.escape
    css = ("body{font-family:system-ui,Arial;margin:2rem;color:#1b1f23}table{border-collapse:collapse;width:100%;margin:1rem 0}"
           "th,td{border:1px solid #d0d7de;padding:6px 8px;font-size:14px;vertical-align:top}th{background:#f6f8fa}"
           ".PASS{background:#dafbe1}.FAIL{background:#ffebe9}.MANUAL{background:#fff8c5}.NA{background:#eee}"
           "pre{background:#f6f8fa;padding:10px;overflow:auto}small{color:#57606a}")
    p = [f"<html><head><meta charset='utf-8'><title>Informe CIS</title><style>{css}</style></head><body>",
         f"<h1>Informe de cumplimiento CIS</h1><p>{e(rep['benchmark'])}<br>Modo: <b>{e(rep['mode'])}</b> · "
         f"Generado: {e(rep['generated'])}</p>"]
    for d in rep["devices"]:
        post = {r["id"]: r for r in d["post"]} if d.get("post") else None
        p.append(f"<h2>{e(d['name'])} <small>{e(d['host'])} · {e(d['role'])}</small></h2>")
        s = f"Cumplimiento antes: <b>{d['score_pre']}%</b>"
        if post is not None:
            s += f" · después: <b>{d['score_post']}%</b>"
        p.append(f"<p>{s}</p>")
        p.append("<table><tr><th>ID</th><th>Control</th><th>Ref. CIS</th><th>Antes</th>"
                 + ("<th>Después</th>" if post is not None else "") + "<th>Detalle / justificación</th></tr>")
        for r in d["pre"]:
            cell = f"<td class='{r['status'].replace('/', '')}'>{r['status']}</td>"
            if post is not None:
                a = post.get(r["id"], {"status": "-"})["status"]
                cell += f"<td class='{a.replace('/', '')}'>{a}</td>"
            det = e(r["detail"]) + f"<br><small>{e(r['why'])}</small>"
            p.append(f"<tr><td>{r['id']}</td><td>{e(r['title'])}</td><td>{e(r['ref'])}</td>{cell}<td>{det}</td></tr>")
        p.append("</table>")
        if d.get("applied"):
            p.append("<details open><summary>Comandos aplicados</summary><pre>" + e("\n".join(to_cli(d["applied"]))) + "</pre></details>")
        if d.get("errors"):
            p.append("<p><b>Errores del equipo:</b></p><pre>" + e("\n".join(d["errors"])) + "</pre>")
    p.append("</body></html>")
    return "\n".join(p)


def list_controls() -> None:
    print("| ID | Control | Ref. CIS* | Por qué se aplica | Equipo |")
    print("|---|---|---|---|---|")
    for c in CONTROLS:
        print(f"| {c.id} | {c.title} | {c.ref} | {c.why} | {'/'.join(c.roles)} |")


# ----------------------------------------------------------------------------
# Flujo principal
# ----------------------------------------------------------------------------
def build_targets(args) -> list[dict]:
    if args.offline:
        devs = []
        for item in args.offline:
            path, role = item, "router"
            if ":" in item and item.rsplit(":", 1)[1] in ("router", "switch", "both", "firewall"):
                path, role = item.rsplit(":", 1)
            devs.append({"name": Path(path).stem, "host": path, "role": role, "offline_file": path, "params": {}})
        return devs
    inv = json.load(open(args.inventory, encoding="utf-8"))
    return [{**d, "params": {**inv.get("params", {}), **d.get("params", {})}} for d in inv["devices"]]


def main() -> int:
    ap = argparse.ArgumentParser(description="Auditoría y hardening CIS Cisco IOS",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--mode", choices=["audit", "remediate"], default="audit")
    ap.add_argument("--inventory", default="inventory.json")
    ap.add_argument("--offline", nargs="+", metavar="ARCHIVO[:ROL]")
    ap.add_argument("--only", help="IDs de controles separados por coma (ej. MGT-08,CTL-01)")
    ap.add_argument("--yes", "-y", action="store_true", help="no pedir confirmación al remediar")
    ap.add_argument("--outdir", default="reports")
    ap.add_argument("--list-controls", action="store_true")
    args = ap.parse_args()

    if args.list_controls:
        list_controls()
        return 0

    only = set(args.only.split(",")) if args.only else None
    targets = build_targets(args)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = Path(args.outdir)
    (outdir / "backups").mkdir(parents=True, exist_ok=True)

    report = {"generated": dt.datetime.now().isoformat(timespec="seconds"), "mode": args.mode,
              "benchmark": BENCHMARK, "devices": []}
    print(f"=== {BENCHMARK} | modo: {args.mode.upper()} ===")

    for dev in targets:
        params = {**DEFAULT_PARAMS, **dev.get("params", {}), "new_enable_secret": bool(os.environ.get("CIS_ENABLE_NEW"))}
        role = dev.get("role", "router")
        print(f"\n>> {dev['name']} ({dev['host']}) rol={role}")
        entry = {"name": dev["name"], "host": dev["host"], "role": role, "applied": [], "errors": [], "post": None}
        conn = None
        try:
            if dev.get("offline_file"):
                text = Path(dev["offline_file"]).read_text(encoding="utf-8", errors="ignore")
            else:
                is_fw = role == "firewall"
                creds = get_creds(dev.get("cred_prefix", "FGT" if is_fw else "CIS"), ask_enable=not is_fw)
                conn = connect({**dev, "role": role}, creds)
                text = conn.send_command("show full-configuration" if is_fw else "show running-config",
                                         read_timeout=180)
        except Exception as ex:
            print(f"   ERROR de conexión/lectura: {ex}")
            entry["errors"].append(f"conexión: {ex}")
            entry["pre"], entry["score_pre"] = [], 0
            report["devices"].append(entry)
            continue

        (outdir / "backups" / f"{dev['name']}_{ts}.cfg").write_text(text, encoding="utf-8")
        cfg = parse_config(text, role)
        pre = run_audit(cfg, role, params, only)
        entry["pre"], entry["score_pre"] = pre, score(pre)
        print_results("ANTES", pre)

        if args.mode == "remediate":
            cmds = [c for r in pre if r["status"] == FAIL for c in r["fix"]]
            if not cmds:
                print("\n   Nada que remediar automáticamente.")
            else:
                print("\n   Comandos a aplicar:")
                print("\n".join("     " + c for c in to_cli(cmds)))
                go = args.yes or input(f"\n   ¿Aplicar {len(cmds)} comandos en {dev['name']}? [s/N]: ").lower() in ("s", "y", "si")
                if go:
                    entry["applied"] = cmds
                    if conn:
                        entry["errors"] = push(conn, cmds)
                        if role != "firewall":      # FortiOS guarda automáticamente
                            conn.save_config()
                        text2 = conn.send_command("show full-configuration" if role == "firewall"
                                                  else "show running-config", read_timeout=180)
                    else:
                        cfg.apply(cmds)
                        text2 = cfg.to_text()
                        (outdir / f"{dev['name']}-hardened.cfg").write_text(text2, encoding="utf-8")
                    post = run_audit(parse_config(text2, role), role, params, only)
                    entry["post"], entry["score_post"] = post, score(post)
                    print_results("DESPUÉS", post)
                    if entry["errors"]:
                        print("   Errores reportados por el equipo:", *entry["errors"], sep="\n     ")
                else:
                    print("   Omitido por el usuario.")
        if conn:
            conn.disconnect()
        report["devices"].append(entry)

    base = outdir / f"cis_{args.mode}_{ts}"
    base.with_suffix(".json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    base.with_suffix(".html").write_text(html_report(report), encoding="utf-8")
    print(f"\nInforme: {base}.html  |  {base}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
