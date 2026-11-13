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
