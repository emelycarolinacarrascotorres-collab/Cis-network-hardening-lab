# ⚙️ Running-configs

[🏠 Inicio](../README.md) · [📘 Configuración inicial](../docs/03-configuracion.md)

Configuraciones de los dispositivos del laboratorio, obtenidas con `show running-config` (Cisco) y `show full-configuration` (FortiGate).

```text
configs/
├── router/     R1-antes.cfg · R1-despues.cfg
├── switch/     SW1-antes.cfg · SW1-despues.cfg
└── firewall/   FW1-antes.cfg · FW1-despues.cfg
```

| Archivo | Dispositivo | Estado | Líneas |
|---|---|---|:---:|
| [`router/R1-antes.cfg`](router/R1-antes.cfg) | R1 | Antes del hardening | 115 |
| [`router/R1-despues.cfg`](router/R1-despues.cfg) | R1 | Después del hardening | 140 |
| [`switch/SW1-antes.cfg`](switch/SW1-antes.cfg) | SW1 | Antes del hardening | 176 |
| [`switch/SW1-despues.cfg`](switch/SW1-despues.cfg) | SW1 | Después del hardening | 216 |
| [`firewall/FW1-antes.cfg`](firewall/FW1-antes.cfg) | FW1 | Antes del hardening | 1472 |
| [`firewall/FW1-despues.cfg`](firewall/FW1-despues.cfg) | FW1 | Después del hardening | 1899 |

## 🔒 Saneamiento aplicado

Antes de publicar se reemplazaron por `<REDACTED>`: el `enable password`, las contraseñas de usuarios locales (incluidos los hashes tipo 7, que son reversibles) y los valores `ENC` de FortiOS. Las direcciones MAC aprendidas por *port-security* en SW1 se conservan. Todo lo demás se conservó sin cambios (se normalizaron los saltos de línea a LF). Las *communities* SNMP `public`/`private` se conservan porque son parte del hallazgo corregido.

## ⚠️ Nota sobre los archivos del FortiGate

`FW1-antes.cfg` y `FW1-despues.cfg` son copias **parciales** de `show full-configuration`: no incluyen secciones como `system snmp sysinfo`, `system ntp`, `system auto-install`, `log syslogd setting` ni `firewall policy`. Los resultados de esos controles provienen de los informes del script ([`reports/`](../reports)), que leyó la configuración completa del equipo.

## Convención de nombres

`<dispositivo>-<estado>.cfg` → `R1-antes.cfg`, `R1-despues.cfg`
