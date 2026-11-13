[🏠 Inicio](../README.md) · [◀ Resultados](06-resultados.md)

# 🧠 07 · Conclusiones y aprendizajes

---

## Conclusiones

1. El hardening con el script elevó el cumplimiento CIS en los tres equipos: **R1** 4.3 % → 78.3 %, **SW1** 8.3 % → 75.0 % y **FW1** 30.8 % → 92.3 %.
2. Se remediaron **41 controles** (R1: 17, SW1: 16, FW1: 8).
3. Los resultados por debajo del 100 % se deben a controles manuales (`MGT-03`, `MGT-05`), a **falsos negativos del script confirmados con las configuraciones** (valores por defecto de IOS en `MGT-06`, `MGT-07` y `MGT-15`; sintaxis `portfast edge` en `L2-01`) y a `FGT-04`, que FortiOS 7.0.9 no expone.
   
## Referencias

- CIS Benchmarks: <https://www.cisecurity.org/cis-benchmarks>

