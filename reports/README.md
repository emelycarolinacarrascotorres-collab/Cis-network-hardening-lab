# 📊 Informes

[🏠 Inicio](../README.md) · [📊 Resultados](../docs/06-resultados.md)

Informes generados por [`scripts/cis_hardening.py`](../scripts/cis_hardening.py). Los `.html` se abren en el navegador (descárguelos o clone el repositorio: GitHub no los renderiza como página).

| Carpeta | Contenido |
|---|---|
| [`auditoria-inicial/`](auditoria-inicial) | Auditoría previa al hardening (2026-11-12 00:00:33) · JSON y HTML |
| [`auditoria-final/`](auditoria-final) | Auditoría posterior al hardening (2026-11-12 16:49:38) · JSON y HTML |
| [`comparativa/`](comparativa) | Informe antes/después armado con las dos auditorías reales |
| [`ejemplos-offline/`](ejemplos-offline) | Ejemplos generados sobre configuraciones de prueba (`scripts/samples/`), **no** sobre el laboratorio |

| Auditoría | R1 | SW1 | FW1 |
|---|:---:|:---:|:---:|
| Inicial | 4.3 % | 8.3 % | 33.3 % (15 controles) · 30.8 % (13 evaluables en ambas fases) |
| Final | 78.3 % | 75.0 % | 92.3 % (13 controles) |

> Los `.html` de `auditoria-inicial`, `auditoria-final` y `comparativa` se generaron a partir de los JSON con la función `html_report` del propio script.
> `reports/backups/` (respaldos de configuración que crea el script) está excluido por `.gitignore`.

## Pendiente

- El informe de la ejecución `remediate` (con comandos aplicados y errores del equipo), si existe.
