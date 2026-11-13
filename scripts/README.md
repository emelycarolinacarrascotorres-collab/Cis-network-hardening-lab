# 📜 Scripts

[🏠 Inicio](../README.md) · [📘 Hardening](../docs/04-hardening.md)

| Script | Lenguaje | Propósito |
|---|---|---|
| [`cis_hardening.py`](cis_hardening.py) | Python 3 | Audita los equipos contra una selección de controles del CIS Cisco IOS Benchmark y, opcionalmente, aplica las correcciones. Genera informes HTML y JSON. |
| [`inventory.json`](inventory.json) | JSON | Equipos del laboratorio (R1, SW1 y FW1: nombre, IP, rol, tipo de conexión) y parámetros de red. **No contiene credenciales.** |
| [`samples/`](samples) | Cisco IOS / FortiOS | Configuraciones de ejemplo (`show running-config` débiles) para probar el script en modo `--offline` sin laboratorio. **No son los running-configs del laboratorio** (esos están en `../running-configs/`). |

## Modos de ejecución

| Modo | Qué hace | ¿Modifica equipos? |
|---|---|---|
| `--mode audit` | Escanea y genera informe de cumplimiento | ❌ No |
| `--mode remediate` | Respalda, aplica las reglas que fallan, re-escanea y genera informe antes/después | ✅ Sí (pide confirmación) |

## Uso

```bash
pip install netmiko            # para conexión real (con IOS antiguo: paramiko==3.5.1)

# Credenciales por variables de entorno (no se guardan en archivos)
#   PowerShell:  $env:CIS_USER="..."; $env:CIS_PASS="..."; $env:CIS_ENABLE="..."
#   Linux/macOS: export CIS_USER=... CIS_PASS=... CIS_ENABLE=...

# Ejecutar desde la RAÍZ del repositorio: los informes se guardan en ./reports
python scripts/cis_hardening.py --inventory scripts/inventory.json --mode audit
python scripts/cis_hardening.py --inventory scripts/inventory.json --mode remediate
python scripts/cis_hardening.py --list-controls

# Sin laboratorio (archivos de configuración de prueba)
python scripts/cis_hardening.py --offline scripts/samples/R1-baseline.cfg:router scripts/samples/SW1-baseline.cfg:switch scripts/samples/FW1-baseline.cfg:firewall --mode remediate --outdir /tmp/prueba
```

## FortiGate

- En el inventario el equipo lleva `"role": "firewall"` y `"device_type": "fortinet"`.
- Credenciales propias: `FGT_USER` y `FGT_PASS` (no usa *enable*).
- Lee la configuración con `show full-configuration` y aplica los cambios con los comandos `config / edit / set`. FortiOS guarda automáticamente.
- Parámetros opcionales en `inventory.json` (`params`): `fw_trusthost` (red permitida para administrar, formato `IP MÁSCARA`) y `fw_hostname`.
- **Limitación:** no soporta FortiGate con **VDOM** habilitado (la configuración queda anidada por VDOM).
- `FGT-07` (`trusthost`) restringe el login de cada administrador a una red: ejecute el script desde esa red o perderá el acceso remoto.
- `FGT-14` (política ANY-ANY-ALL) queda siempre como **MANUAL**: decidir qué tráfico se permite es diseño, no un ajuste automático.

> Para conexión por Telnet cambie `"device_type"` a `"cisco_ios_telnet"` en `inventory.json`.

El script se ejecutó en el laboratorio con la conexión indicada en `inventory.json`. **[AGREGAR]** los comandos exactos (SSH o Telnet) usados en cada fase.
