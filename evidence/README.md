# 🖼️ Evidencias

[🏠 Inicio](../README.md) · [🧪 Pruebas](../docs/05-pruebas.md)

```text
evidence/
├── 01-topologia/          topología en GNS3
├── 02-configuracion/      IPs, interfaces y conectividad
├── 03-auditoria-inicial/  auditoría inicial de R1, SW1 y FW1
├── 04-hardening/          comandos aplicados por el script
├── 05-auditoria-final/    auditoría final de R1, SW1 y FW1
└── 06-pruebas/            capturas de las pruebas funcionales
```

| Captura | Qué muestra |
|---|---|
| [`01-topologia/01-topologia-gns3.png`](01-topologia/01-topologia-gns3.png) | Topología completa en GNS3 |
| [`02-configuracion/01-ipconfig-pc-admin.png`](02-configuracion/01-ipconfig-pc-admin.png) | IP de PC-Admin (10.25.20.10) |
| [`02-configuracion/02-sw1-show-ip-interface-brief.png`](02-configuracion/02-sw1-show-ip-interface-brief.png) | Interfaces de SW1 |
| [`02-configuracion/03-r1-show-ip-interface-brief.png`](02-configuracion/03-r1-show-ip-interface-brief.png) | Interfaces de R1 |
| [`02-configuracion/04-ping-desde-pc-admin.png`](02-configuracion/04-ping-desde-pc-admin.png) | Ping a FW1 y PC-User |
| [`03-auditoria-inicial/01-audit-inicial-r1.png`](03-auditoria-inicial/01-audit-inicial-r1.png) | R1 · 4.3 % |
| [`03-auditoria-inicial/02-audit-inicial-sw1.png`](03-auditoria-inicial/02-audit-inicial-sw1.png) | SW1 · 8.3 % |
| [`03-auditoria-inicial/03-audit-inicial-fw1.png`](03-auditoria-inicial/03-audit-inicial-fw1.png) | FW1 · 30.8 % |
| [`04-hardening/01-r1-comandos-aplicados.png`](04-hardening/01-r1-comandos-aplicados.png) | Comandos del script para R1 |
| [`04-hardening/02-r1-comandos-aplicados-parcial.png`](04-hardening/02-r1-comandos-aplicados-parcial.png) | Versión parcial de la captura anterior |
| [`04-hardening/03-fw1-comandos-aplicados.png`](04-hardening/03-fw1-comandos-aplicados.png) | Comandos del script para FW1 |
| [`05-auditoria-final/01-audit-final-r1.png`](05-auditoria-final/01-audit-final-r1.png) | R1 · 78.3 % |
| [`05-auditoria-final/02-audit-final-sw1.png`](05-auditoria-final/02-audit-final-sw1.png) | SW1 · 75.0 % |
| [`05-auditoria-final/03-audit-final-fw1.png`](05-auditoria-final/03-audit-final-fw1.png) | FW1 · 92.3 % |
| [`06-pruebas/01-telnet-puerto23-cerrado-r1.png`](06-pruebas/01-telnet-puerto23-cerrado-r1.png) | Puerto 23 cerrado y 22 abierto en R1 |
| [`06-pruebas/01-telnet-puerto23-cerrado-sw1.png`](06-pruebas/01-telnet-puerto23-cerrado-sw1.png) | Puerto 23 cerrado y 22 abierto en SW1 (con el error de intercambio de claves previo) |
| [`06-pruebas/02-ssh-error-kex-r1.png`](06-pruebas/02-ssh-error-kex-r1.png) | Error *no matching key exchange method* del cliente SSH de Windows |
| [`06-pruebas/04-snmp-password-r1.png`](06-pruebas/04-snmp-password-r1.png) | R1 sin SNMP; contraseñas tipo 7 (ocultas) |
| [`06-pruebas/04-snmp-password-sw1.png`](06-pruebas/04-snmp-password-sw1.png) | SW1 sin SNMP; contraseñas tipo 7 (ocultas) |
| [`06-pruebas/05-http-cerrado-r1-sw1.png`](06-pruebas/05-http-cerrado-r1-sw1.png) | Puerto 80 cerrado en R1 y SW1 |
| [`06-pruebas/06-cdp-r1.png`](06-pruebas/06-cdp-r1.png) | CDP deshabilitado en R1 |
| [`06-pruebas/06-cdp-sw1.png`](06-pruebas/06-cdp-sw1.png) | CDP deshabilitado en SW1 |
| [`06-pruebas/07-show-ip-ssh-r1.png`](06-pruebas/07-show-ip-ssh-r1.png) | SSH 2.0, timeout 60, retries 3 en R1 |
| [`06-pruebas/07-show-ip-ssh-sw1.png`](06-pruebas/07-show-ip-ssh-sw1.png) | SSH 2.0, timeout 60, retries 3 en SW1 |
| [`06-pruebas/07-show-line-con0-r1.png`](06-pruebas/07-show-line-con0-r1.png) | Consola de R1 (Idle EXEC 10 min) con CDP y SNMP |
| [`06-pruebas/07-show-line-con0-sw1.png`](06-pruebas/07-show-line-con0-sw1.png) | Consola de SW1 (Idle EXEC 10 min) |
| [`06-pruebas/07-show-line-vty-r1.png`](06-pruebas/07-show-line-vty-r1.png) | VTY de R1 (Idle EXEC 10 min, solo SSH) |
| [`06-pruebas/07-show-line-vty-sw1.png`](06-pruebas/07-show-line-vty-sw1.png) | VTY de SW1 (Idle EXEC 10 min, solo SSH) |
| [`06-pruebas/11-port-security-sw1.png`](06-pruebas/11-port-security-sw1.png) | Port-security en SW1 |
| [`06-pruebas/12-bpduguard-sw1.png`](06-pruebas/12-bpduguard-sw1.png) | BPDU Guard por defecto en SW1 |
| [`06-pruebas/13-fw-trusthost-pc-user-timeout.png`](06-pruebas/13-fw-trusthost-pc-user-timeout.png) | ipconfig de PC-User y SSH al FortiGate con timeout |
| [`06-pruebas/14-fw-telnet-http-cerrados.png`](06-pruebas/14-fw-telnet-http-cerrados.png) | Puertos 23 y 80 cerrados en el FortiGate |
| [`06-pruebas/15-fw-password-policy.png`](06-pruebas/15-fw-password-policy.png) | Política de contraseñas del FortiGate |
| [`06-pruebas/15-fw-snmp-sysinfo.png`](06-pruebas/15-fw-snmp-sysinfo.png) | SNMP sysinfo del FortiGate |

> Las capturas de `06-pruebas` que mostraban hashes tipo 7 (reversibles) se editaron para ocultarlos.
> El script rotula **ANTES** a la lectura inicial de cada ejecución, también en las auditorías finales.

## Convención de nombres

`NN-descripcion-corta.png` (minúsculas, sin espacios ni acentos). Las capturas de pruebas van en `06-pruebas/`, p. ej. `01-telnet-rechazado.png`.
