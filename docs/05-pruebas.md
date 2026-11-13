[🏠 Inicio](../README.md) · [◀ Hardening](04-hardening.md) · [Resultados ▶](06-resultados.md)

# 🧪 05 · Pruebas

---

**Leyenda:** ✅ realizada con evidencia · 🟡 evidencia parcial · ⬜ pendiente. Las capturas están en [`evidence/06-pruebas/`](../evidence/06-pruebas). Los hashes tipo 7 que mostraban algunas capturas se ocultaron (son reversibles).

## Pruebas realizadas

| # | Prueba | Resultado esperado | Resultado obtenido | Control | Estado |
|---|---|---|---|---|:---:|
| A | Re-ejecutar el script en modo `audit` | Cumplimiento superior al inicial | R1 78.3 % · SW1 75.0 % · FW1 92.3 % ([capturas](../evidence/05-auditoria-final)) | Todos | ✅ |
| B | Conectividad de PC-Admin a FW1 y PC-User | Respuesta a ping | 3/3 a `10.25.0.2` y 4/4 a `10.25.6.10` ([captura](../evidence/02-configuracion/04-ping-desde-pc-admin.png)) | — | ✅ |
| 1 | Telnet cerrado en R1 y SW1 | Puerto 23 inaccesible | `Test-NetConnection` desde PC-Admin: puerto **23 `False`** y puerto **22 `True`** en [R1](../evidence/06-pruebas/01-telnet-puerto23-cerrado-r1.png) y [SW1](../evidence/06-pruebas/01-telnet-puerto23-cerrado-sw1.png) | MGT-08 | ✅ |
| 4 | Sin SNMP por defecto y contraseñas cifradas | Sin `snmp-server community`; `service password-encryption` | [R1](../evidence/06-pruebas/04-snmp-password-r1.png) y [SW1](../evidence/06-pruebas/04-snmp-password-sw1.png): sin líneas `snmp-server`; `enable password` y usuario local siguen en **tipo 7 (reversible)** | MGT-11 · MGT-04 | ✅ (SNMP) · 🟡 (claves) |
| 5 | HTTP cerrado | Puerto 80 inaccesible | `Test-NetConnection` a `10.25.20.1` y `10.25.20.2`: puerto 80 `False` ([captura](../evidence/06-pruebas/05-http-cerrado-r1-sw1.png)) | MGT-12 | ✅ |
| 6 | CDP deshabilitado | `% CDP is not enabled` | R1 ([captura](../evidence/06-pruebas/06-cdp-r1.png)) y SW1 ([captura](../evidence/06-pruebas/06-cdp-sw1.png)) | CTL-01 | ✅ |
| 7 | **Valores por defecto de IOS** | *Idle EXEC* 00:10:00 y *retries* 3 | Consola y VTY con **Idle EXEC 00:10:00** en R1 ([con 0](../evidence/06-pruebas/07-show-line-con0-r1.png) · [vty](../evidence/06-pruebas/07-show-line-vty-r1.png)) y SW1 ([con 0](../evidence/06-pruebas/07-show-line-con0-sw1.png) · [vty](../evidence/06-pruebas/07-show-line-vty-sw1.png)); VTY con `Allowed input transports are ssh`; `show ip ssh`: SSH 2.0, timeout 60 s, **retries 3** en [R1](../evidence/06-pruebas/07-show-ip-ssh-r1.png) y [SW1](../evidence/06-pruebas/07-show-ip-ssh-sw1.png) | MGT-06 · 07 · 08 · 13 · 14 · 15 | ✅ |
| 11 | Port-security en SW1 | Habilitado en puertos de acceso | `Gi0/1`, `Gi0/2`, `Gi0/3`: máximo 2, 0 violaciones, acción `Restrict` ([captura](../evidence/06-pruebas/11-port-security-sw1.png)) | L2-02 | ✅ |
| 12 | BPDU Guard en SW1 | Habilitado por defecto | `Portfast Edge BPDU Guard Default is enabled` ([captura](../evidence/06-pruebas/12-bpduguard-sw1.png)) | L2-01 | ✅ |
| 13 | Administración del FortiGate restringida | Login denegado fuera de `trusthost` | Desde **PC-User** (10.25.6.10): `ssh admin@10.25.0.2` → *Connection timed out* ([captura](../evidence/06-pruebas/13-fw-trusthost-pc-user-timeout.png)). Falta el contraste desde PC-Admin | FGT-07 | 🟡 |
| 14 | Telnet y HTTP cerrados en el FortiGate | Puertos 23 y 80 inaccesibles | Desde PC-Admin a `10.25.0.2`: ambos `False` ([captura](../evidence/06-pruebas/14-fw-telnet-http-cerrados.png)) | FGT-08 | ✅ |
| 15 | Configuración de seguridad del FortiGate | Política de contraseñas y SNMP | `show system password-policy`: `status enable`, longitud 12 y complejidad ([captura](../evidence/06-pruebas/15-fw-password-policy.png)); `show system snmp sysinfo`: sección con valores por defecto ([captura](../evidence/06-pruebas/15-fw-snmp-sysinfo.png)). Faltan banner y bloqueo de admin | FGT-09 · FGT-10 · FGT-02 · FGT-06 | 🟡 |

## Pruebas pendientes

| # | Prueba | Cómo hacerla | Resultado esperado | Control | Estado |
|---|---|---|---|---|:---:|
| 2 | SSH permitido desde la VLAN 99 | Desde PC-Admin: `ssh -oKexAlgorithms=+diffie-hellman-group14-sha1 -oHostKeyAlgorithms=+ssh-rsa admin@10.25.20.1` | Conecta y muestra el aviso de acceso autorizado | MGT-09 · MGT-10 | ⬜ |
| 3 | SSH bloqueado desde otra VLAN | Desde PC-User, el mismo comando; luego en R1 `show access-lists CIS-VTY-ACL` | No conecta; el contador de `deny any log` aumenta | MGT-09 | ⬜ |
| 8 | Logging en R1 y SW1 | `show logging` | Buffer de 64000 bytes y servidor `10.25.20.10` | CTL-04 · CTL-05 | ⬜ |
| 9 | Syslog recibido | Wireshark en PC-Admin con `udp.port == 514` y generar un evento en R1 | Paquetes syslog hacia `10.25.20.10` | CTL-05 · CTL-06 | ⬜ |
| 10 | Proxy ARP deshabilitado | `show ip interface Gi2/0.10 \| include Proxy` en R1 | `Proxy ARP is disabled` | DAT-02 | ⬜ |
| 13b | Contraste de `trusthost` | Desde PC-Admin: `ssh admin@10.25.0.2`; desde PC-User: `ping 10.25.0.2` | PC-Admin entra; el ping desde PC-User responde (descarta un problema de ruta) | FGT-07 | ⬜ |
| 15b | Resto de la configuración del FortiGate | `show full-configuration system global` y `system snmp sysinfo` | `pre-login-banner enable`, `admin-lockout-duration 900`, `set status disable` | FGT-02 · FGT-06 · FGT-10 | ⬜ |
| 16 | Syslog del FortiGate | `show full-configuration log syslogd setting` y Wireshark en PC-Admin | Estado habilitado, servidor `10.25.20.10`, paquetes recibidos | FGT-11 | ⬜ |
| 17 | *(Opcional)* Contraseña débil rechazada | `config system admin` → `edit prueba` → `set password abc` | El equipo la rechaza; borrar el usuario después | FGT-09 | ⬜ |
| 18 | *(Opcional)* Bloqueo por intentos fallidos | 3 intentos fallidos desde PC-Admin | Cuenta bloqueada 15 min (la consola de GNS3 sigue disponible) | FGT-05 · FGT-06 | ⬜ |
| 19 | La red sigue funcionando | Ping entre PC-User, el servidor y PC-Admin | Respuesta en todos los casos | — | ⬜ |
| 20 | Auditoría final definitiva | `python scripts/cis_hardening.py --inventory scripts/inventory.json --mode audit` | Cumplimiento final de los tres equipos | Todos | ⬜ |

## Notas

- **Prueba 7:** estas capturas **confirman en los equipos** que `MGT-06`, `MGT-07`, `MGT-15` (y `L2-01`, prueba 12) están aplicados aunque el script los marque como incumplidos. Ver [Resultados](06-resultados.md).
- **Prueba 5:** en SW1 `ip http secure-server` sigue activo, por lo que el puerto **443** respondería; es una observación, no un fallo de los controles seleccionados.
- **Prueba 13:** el contraste *antes/después* de `http` en el FortiGate ocurrió en `port1` (lado NAT), que PC-Admin no alcanza; esa evidencia está en el [cambio de configuración](06-resultados.md).
- **Prueba 18:** hágala al final y desde PC-Admin; un bloqueo de 15 minutos le impedirá administrar el FortiGate por red.
- El cliente SSH de Windows rechaza por defecto los intercambios de claves SHA-1 que ofrece este IOS ([captura del error](../evidence/06-pruebas/02-ssh-error-kex-r1.png)); por eso los comandos SSH llevan las opciones `-oKexAlgorithms` y `-oHostKeyAlgorithms`.
