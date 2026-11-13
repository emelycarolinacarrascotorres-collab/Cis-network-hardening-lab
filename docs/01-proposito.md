[🏠 Inicio](../README.md) · [Topología ▶](02-topologia.md)

# 🎯 01 · Propósito del laboratorio

---

## Propósito

Construir una red con **router, switch y firewall**, evaluar su nivel de seguridad frente al **CIS Benchmark**, aplicar recomendaciones de *hardening*, documentarlas y comprobar su efecto, apoyándose en un **script de Python** que automatiza el análisis y la corrección.

## Objetivos específicos

| # | Objetivo | Cómo se abordó |
|---|---|---|
| 1 | Crear una red con router, switch y/o firewall | R1, SW1 y FW1 en GNS3 → [02-topologia.md](02-topologia.md) |
| 2 | Analizar la red con una herramienta basada en el CIS Benchmark | Script `cis_hardening.py`, modo `audit` → [`reports/`](../reports) |
| 3 | Aplicar recomendaciones de hardening | 40 controles (25 Cisco IOS · 15 FortiGate) → [04-hardening.md](04-hardening.md) |
| 4 | Documentar qué se aplicó y por qué | Fichas por control → [`docs/controles/`](controles) |
| 5 | Probar las recomendaciones | Plan de pruebas → [05-pruebas.md](05-pruebas.md) |
| 6 | Automatizar el escaneo con informe sin aplicar y aplicando reglas | Modos `audit` y `remediate` → [`scripts/`](../scripts) |

## Aspectos de seguridad trabajados

| Aspecto | Dispositivos |
|---|---|
| 🔑 Autenticación y protección de credenciales | R1 · SW1 · FW1 |
| 🚪 Control de acceso a la administración (SSH, ACL, `trusthost`, timeouts) | R1 · SW1 · FW1 |
| 🛡️ Reducción de superficie de ataque (servicios innecesarios) | R1 · SW1 · FW1 |
| 📝 Logging y sincronización horaria | R1 · SW1 · FW1 |
| 📡 SNMP | R1 · SW1 · FW1 |
| 🔀 Seguridad en capa 2 | SW1 |
| 🔥 Políticas de firewall | FW1 |

## ¿Qué se esperaba comprobar?

1. Que el **porcentaje de cumplimiento** aumentara respecto al estado inicial.
2. Que los accesos inseguros (Telnet, SNMP por defecto, HTTP) dejaran de funcionar.
3. Que la administración solo fuera posible desde la **red de gestión** (VLAN 99).
4. Que la red **siguiera funcionando** (el hardening no debe romper el servicio).

## Alcance y límites

- Entorno simulado en **GNS3**.
- Se implementó una **selección** de controles CIS, no el benchmark completo.
- Hay pruebas funcionales pendientes de evidenciar → [05-pruebas.md](05-pruebas.md).
