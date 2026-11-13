[🏠 Inicio](../README.md) · [◀ Resultados](06-resultados.md)

# 🧠 07 · Conclusiones y aprendizajes

---

## Conclusiones

1. El hardening con el script elevó el cumplimiento CIS en los tres equipos: **R1** 4.3 % → 78.3 %, **SW1** 8.3 % → 75.0 % y **FW1** 30.8 % → 92.3 %.
2. Se remediaron **41 controles** (R1: 17, SW1: 16, FW1: 8).
3. Los resultados por debajo del 100 % se deben a controles manuales (`MGT-03`, `MGT-05`), a **falsos negativos del script confirmados con las configuraciones** (valores por defecto de IOS en `MGT-06`, `MGT-07` y `MGT-15`; sintaxis `portfast edge` en `L2-01`) y a `FGT-04`, que FortiOS 7.0.9 no expone.
4. **[AGREGAR]** si el hardening afectó la conectividad o la administración.

## Lo que aprendí

- **[AGREGAR]** aprendizaje sobre el CIS Benchmark y el hardening.
- **[AGREGAR]** aprendizaje sobre automatización con Python y Netmiko.
- **[AGREGAR]** aprendizaje sobre VLAN, ACL, SSH y firewall.
- Un auditor automático puede equivocarse: los valores por defecto que el equipo no muestra producen falsos negativos y hay que verificarlos en el dispositivo.

## Limitaciones

- Se aplicó una **selección** de controles CIS, no el benchmark completo.
- Entorno simulado; el comportamiento puede variar en equipos físicos.
- Pruebas funcionales pendientes de evidenciar → [05-pruebas.md](05-pruebas.md).

## Mejoras futuras

- Ajustar los chequeos que dependen de valores por defecto (`MGT-06`, `MGT-07`, `MGT-15`).
- **[AGREGAR]** otras mejoras (NTP en IOS, AAA centralizado, políticas de firewall más específicas).

## Referencias

- CIS Benchmarks: <https://www.cisecurity.org/cis-benchmarks>
- **[AGREGAR]** otras fuentes utilizadas.
