# 🛡️ Controles CIS · FW1 (firewall)

[🏠 README](../../README.md) · [📘 Hardening](../04-hardening.md) · [📊 Resultados](../06-resultados.md)

---

**Auditoría inicial:** 33.3 % (5/15 controles) &nbsp;→&nbsp; **Auditoría final:** 92.3 % (12/13 controles)

Fuentes: [`reports/auditoria-inicial`](../../reports/auditoria-inicial) · [`reports/auditoria-final`](../../reports/auditoria-final) · configuración: [`configs/firewall/FW1-antes.cfg`](../../configs/firewall/FW1-antes.cfg) → [`configs/firewall/FW1-despues.cfg`](../../configs/firewall/FW1-despues.cfg)

> **Leyenda:** ✅ cumple · ❌ no cumple · 🟡 requiere acción manual · ⚪ no evaluable. Los comandos listados son los que genera el script a partir de la configuración *antes*; el resultado real lo determina la auditoría final.

> **Nota sobre los porcentajes:** la auditoría inicial registró 33.3 % sobre 15 controles (existía una política de firewall, por lo que `FGT-13` y `FGT-14` se evaluaron). En la auditoría final esos dos controles son N/A (sin políticas). Sobre los **13 controles evaluables en ambas fases** el cumplimiento inicial fue de **30.8 %**, cifra que coincide con la [captura de la auditoría inicial](../../evidence/03-auditoria-inicial/03-audit-inicial-fw1.png).

## Resumen

| ID | Control | Antes | Después | Estado |
|---|---|:---:|:---:|---|
| `FGT-01` | Hostname distinto al valor por defecto | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-02` | Banner previo al login habilitado | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-03` | Timeout de inactividad de administración <= 5 min | ✅ PASS | ✅ PASS | Ya cumplía |
| `FGT-04` | Strong-crypto habilitado | ❌ FAIL | ❌ FAIL | No reflejado en el audit final |
| `FGT-05` | Bloqueo de admin: umbral <= 3 intentos | ✅ PASS | ✅ PASS | Ya cumplía |
| `FGT-06` | Bloqueo de admin: duración >= 900 s | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-07` | Administradores con 'trusthost' restringido | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-08` | Sin Telnet ni HTTP en 'allowaccess' de interfaces | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-09` | Política de contraseñas habilitada (longitud y complejidad) | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-10` | Agente SNMP deshabilitado | ✅ PASS | ✅ PASS | Ya cumplía |
| `FGT-11` | Logs enviados a servidor syslog | ❌ FAIL | ✅ PASS | **Remediado** |
| `FGT-12` | Sincronización NTP habilitada | ✅ PASS | ✅ PASS | Ya cumplía |
| `FGT-13` | Logging de tráfico en todas las políticas | ✅ PASS | ⚪ N/A | No evaluable al final |
| `FGT-14` | Sin políticas ANY-ANY-ALL con 'accept' | 🟡 MANUAL | ⚪ N/A | No evaluable al final |
| `FGT-15` | Auto-instalación por USB deshabilitada | ❌ FAIL | ✅ PASS | **Remediado** |

## Detalle por control

*(Haga clic en cada control para desplegarlo.)*

<details>
<summary><b><code>FGT-01</code></b> · Hostname distinto al valor por defecto &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-01` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** El hostname por defecto revela el modelo y dificulta el inventario y la correlación de logs.
- **Recomendación:** Hostname distinto al valor por defecto
- **Justificación:** Un nombre propio facilita inventario y correlación de logs; el nombre por defecto delata el modelo.
- **Prueba de validación:** `get system status` (Hostname) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Hostname por defecto (actual: FortiGate-VM64-KVM)
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system global
set hostname FW1
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L98: set hostname "FortiGate-VM64-KVM"
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L97: set hostname "FW1"
```

</details>

<details>
<summary><b><code>FGT-02</code></b> · Banner previo al login habilitado &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-02` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Sin aviso legal previo al inicio de sesión se debilita la base legal frente a accesos no autorizados.
- **Recomendación:** Banner previo al login habilitado
- **Justificación:** Aviso legal de acceso autorizado antes de autenticarse.
- **Prueba de validación:** Abrir la página de login o conectar por SSH y comprobar el aviso · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Banner deshabilitado (actual: disable)
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system global
set pre-login-banner enable
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L136: set pre-login-banner disable
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L135: set pre-login-banner enable
```

</details>

<details>
<summary><b><code>FGT-03</code></b> · Timeout de inactividad de administración <= 5 min &nbsp; ✅ → ✅</summary>

- **Identificador:** `FGT-03` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Sesiones de administración abandonadas pueden ser utilizadas por terceros.
- **Recomendación:** Timeout de inactividad de administración <= 5 min
- **Justificación:** Cierra sesiones de administración abandonadas.
- **Prueba de validación:** `show full-configuration system global` → `admintimeout` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ✅ `PASS`
- **Estado:** Ya cumplía

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L32: set admintimeout 5
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L31: set admintimeout 5
```

</details>

<details>
<summary><b><code>FGT-04</code></b> · Strong-crypto habilitado &nbsp; ❌ → ❌</summary>

- **Identificador:** `FGT-04` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Protocolos y cifrados débiles aceptados en la administración.
- **Recomendación:** Strong-crypto habilitado
- **Justificación:** Fuerza protocolos y cifrados robustos (TLS/SSH) en la administración.
- **Prueba de validación:** Verificación manual en el equipo (el parámetro no aparece en `show full-configuration` de FortiOS 7.0.9) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — 'strong-crypto' no visible (use 'show full-configuration')
- **Resultado después:** ❌ `FAIL` — 'strong-crypto' no visible (use 'show full-configuration')
- **Estado:** No reflejado en el audit final

**Configuración que genera el script (no quedó reflejada como cumplida):**

```text
config system global
set strong-crypto enable
end
```

⚠️ El parámetro `strong-crypto` no aparece en la salida de `show full-configuration` (FortiOS 7.0.9 VM), ni antes ni después de aplicar el comando; por eso el script no puede verificarlo. **[AGREGAR verificación manual en el equipo]**

</details>

<details>
<summary><b><code>FGT-05</code></b> · Bloqueo de admin: umbral <= 3 intentos &nbsp; ✅ → ✅</summary>

- **Identificador:** `FGT-05` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Sin límite de intentos fallidos las cuentas de administración son vulnerables a fuerza bruta.
- **Recomendación:** Bloqueo de admin: umbral <= 3 intentos
- **Justificación:** Mitiga fuerza bruta contra las cuentas de administración.
- **Prueba de validación:** `show full-configuration system global` → `admin-lockout-threshold`; fallar la contraseña varias veces · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ✅ `PASS`
- **Estado:** Ya cumplía

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L18: set admin-lockout-threshold 3
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L17: set admin-lockout-threshold 3
```

</details>

<details>
<summary><b><code>FGT-06</code></b> · Bloqueo de admin: duración >= 900 s &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-06` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Un bloqueo demasiado corto permite reanudar rápido los ataques de adivinación de contraseñas.
- **Recomendación:** Bloqueo de admin: duración >= 900 s
- **Justificación:** Un bloqueo suficientemente largo frena los ataques de adivinación de contraseñas.
- **Prueba de validación:** `show full-configuration system global` → `admin-lockout-duration` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Debe ser >= 900 s (actual: 60)
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system global
set admin-lockout-duration 900
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L17: set admin-lockout-duration 60
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L16: set admin-lockout-duration 900
```

</details>

<details>
<summary><b><code>FGT-07</code></b> · Administradores con 'trusthost' restringido &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-07` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** La cuenta de administrador puede iniciar sesión desde cualquier IP (`0.0.0.0/0`).
- **Recomendación:** Administradores con 'trusthost' restringido
- **Justificación:** Cada cuenta admin solo debe poder iniciar sesión desde la red de gestión (evita 0.0.0.0/0).
- **Prueba de validación:** Iniciar sesión desde un host fuera de `10.25.20.0/24` debe fallar · Prueba n.º 15 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [ssh desde PC-User](../../evidence/06-pruebas/13-fw-trusthost-pc-user-timeout.png)
- **Resultado antes:** ❌ `FAIL` — No cumple: admin
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system admin
edit "admin"
set trusthost1 10.25.20.0 255.255.255.0
next
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L1293: set trusthost1 0.0.0.0 0.0.0.0
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L1303: set trusthost1 10.25.20.0 255.255.255.0
```

🟡 Evidencia parcial: desde PC-User (10.25.6.10) `ssh admin@10.25.0.2` termina en *Connection timed out*. Falta el contraste: acceso correcto desde PC-Admin y `ping 10.25.0.2` desde PC-User (para descartar un problema de ruta).

</details>

<details>
<summary><b><code>FGT-08</code></b> · Sin Telnet ni HTTP en 'allowaccess' de interfaces &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-08` · Ref. CIS: FortiGate · Red
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Telnet y HTTP exponen credenciales y sesiones en texto claro en las interfaces.
- **Recomendación:** Sin Telnet ni HTTP en 'allowaccess' de interfaces
- **Justificación:** Telnet y HTTP viajan en claro; la administración debe ser solo por HTTPS/SSH.
- **Prueba de validación:** `Test-NetConnection <IP> -Port 23` y `-Port 80` deben dar `False` · Prueba n.º 14 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [puertos 23 y 80](../../evidence/06-pruebas/14-fw-telnet-http-cerrados.png)
- **Resultado antes:** ❌ `FAIL` — No cumple: port1
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system interface
edit "port1"
set allowaccess ping https ssh fgfm
next
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L261: set allowaccess ping https ssh http fgfm
L366: set allowaccess ping https ssh
L1139: set allowaccess ping fabric
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L260: set allowaccess ping https ssh fgfm
L366: set allowaccess ping https ssh
L1140: set allowaccess ping fabric
```

</details>

<details>
<summary><b><code>FGT-09</code></b> · Política de contraseñas habilitada (longitud y complejidad) &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-09` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Contraseñas cortas o sin complejidad son vulnerables a ataques de diccionario.
- **Recomendación:** Política de contraseñas habilitada (longitud y complejidad)
- **Justificación:** Contraseñas largas y complejas reducen el éxito de ataques de diccionario.
- **Prueba de validación:** `show full-configuration system password-policy`; intentar una contraseña débil · Evidencia: [password-policy](../../evidence/06-pruebas/15-fw-password-policy.png)
- **Resultado antes:** ❌ `FAIL` — Política deshabilitada, longitud < 8 o sin complejidad
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system password-policy
set status enable
set minimum-length 12
set min-lower-case-letter 1
set min-upper-case-letter 1
set min-number 1
set min-non-alphanumeric 1
end
```

**Evidencia en la configuración (antes)** — `configs/firewall/FW1-antes.cfg`:

```text
L277: set status up
L383: set status up
L490: set status up
L598: set status up
L706: set status up
L814: set status up
```

**Evidencia en la configuración (después)** — `configs/firewall/FW1-despues.cfg`:

```text
L276: set status up
L383: set status up
L491: set status up
L599: set status up
L707: set status up
L815: set status up
L915: set status up
L991: set status up
L1070: set status up
L1155: set status up
```

</details>

<details>
<summary><b><code>FGT-10</code></b> · Agente SNMP deshabilitado &nbsp; ✅ → ✅</summary>

- **Identificador:** `FGT-10` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** El agente SNMP v1/v2c no cifra y agrega superficie de ataque si no es necesario.
- **Recomendación:** Agente SNMP deshabilitado
- **Justificación:** Si no se usa, el agente SNMP solo agrega superficie de ataque (y v1/v2c no cifra).
- **Prueba de validación:** `show full-configuration system snmp sysinfo` · Evidencia: [snmp sysinfo](../../evidence/06-pruebas/15-fw-snmp-sysinfo.png)
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ✅ `PASS`
- **Estado:** Ya cumplía

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

ℹ️ `show system snmp sysinfo` devuelve la sección vacía: todos los valores por defecto (estado deshabilitado). Una prueba más clara es `show full-configuration system snmp sysinfo` (muestra `set status disable`).

</details>

<details>
<summary><b><code>FGT-11</code></b> · Logs enviados a servidor syslog &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-11` · Ref. CIS: FortiGate · Logging
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Los logs solo locales se pierden si el equipo se compromete o se reinicia.
- **Recomendación:** Logs enviados a servidor syslog
- **Justificación:** Logs centralizados no se pierden si el equipo se compromete o reinicia.
- **Prueba de validación:** `show full-configuration log syslogd setting`; recibir mensajes en el servidor syslog · Prueba n.º 16 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Syslog remoto deshabilitado o sin servidor
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config log syslogd setting
set status enable
set server "10.25.20.10"
end
```

</details>

<details>
<summary><b><code>FGT-12</code></b> · Sincronización NTP habilitada &nbsp; ✅ → ✅</summary>

- **Identificador:** `FGT-12` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Sin hora correcta no se pueden correlacionar eventos entre equipos.
- **Recomendación:** Sincronización NTP habilitada
- **Justificación:** Hora correcta es indispensable para correlacionar eventos.
- **Prueba de validación:** `show full-configuration system ntp` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ✅ `PASS`
- **Estado:** Ya cumplía

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

</details>

<details>
<summary><b><code>FGT-13</code></b> · Logging de tráfico en todas las políticas &nbsp; ✅ → ⚪</summary>

- **Identificador:** `FGT-13` · Ref. CIS: FortiGate · Políticas
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Sin `logtraffic all` no queda registro del tráfico permitido para análisis forense.
- **Recomendación:** Logging de tráfico en todas las políticas
- **Justificación:** Sin 'logtraffic all' no hay registro del tráfico permitido para análisis forense.
- **Prueba de validación:** Log & Report → Forward Traffic (sesiones registradas) · Prueba n.º 16 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ⚪ `N/A` — sin entradas en 'firewall policy'
- **Estado:** No evaluable al final

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

⚪ No evaluable en la auditoría final: el FortiGate no tenía entradas en `firewall policy`. En la auditoría inicial sí existía al menos una política (control cumplido).

</details>

<details>
<summary><b><code>FGT-14</code></b> · Sin políticas ANY-ANY-ALL con 'accept' &nbsp; 🟡 → ⚪</summary>

- **Identificador:** `FGT-14` · Ref. CIS: FortiGate · Políticas
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Una política ANY-ANY-ALL con `accept` anula el firewall.
- **Recomendación:** Sin políticas ANY-ANY-ALL con 'accept'
- **Justificación:** Una política que permite todo origen, destino y servicio anula el firewall. Requiere diseño manual (qué sí se permite).
- **Prueba de validación:** `show firewall policy` (sin política ANY-ANY-ALL) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** 🟡 `MANUAL` — No cumple: 1 -> requiere acción manual
- **Resultado después:** ⚪ `N/A` — sin entradas en 'firewall policy'
- **Estado:** No evaluable al final

⚪ En la auditoría inicial se detectó una política ANY-ANY-ALL con `accept` (hallazgo manual). En la auditoría final no había políticas, por lo que no es evaluable. **[AGREGAR qué ocurrió con la política]**

</details>

<details>
<summary><b><code>FGT-15</code></b> · Auto-instalación por USB deshabilitada &nbsp; ❌ → ✅</summary>

- **Identificador:** `FGT-15` · Ref. CIS: FortiGate · Sistema
- **Dispositivo:** FW1 (firewall)
- **Riesgo:** Con acceso físico, alguien puede cargar configuración o firmware desde un USB.
- **Recomendación:** Auto-instalación por USB deshabilitada
- **Justificación:** Evita que alguien con acceso físico cargue configuración o firmware desde un USB.
- **Prueba de validación:** `show full-configuration system auto-install` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Auto-instalación por USB habilitada
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
config system auto-install
set auto-install-config disable
set auto-install-image disable
end
```

</details>
