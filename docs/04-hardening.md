[🏠 Inicio](../README.md) · [◀ Configuración](03-configuracion.md) · [Pruebas ▶](05-pruebas.md)

# 🛡️ 04 · Hardening con CIS Benchmark

---

## Herramienta de análisis

| Herramienta | Uso |
|---|---|
| **`cis_hardening.py`** (propia) | Auditoría y remediación de los controles seleccionados en Cisco IOS y FortiOS → [`scripts/`](../scripts) |
| **[AGREGAR]** | CIS-CAT / Nipper / otra, solo si se usó |

## Proceso

```mermaid
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#1E293B","primaryTextColor":"#E2E8F0","primaryBorderColor":"#38BDF8","lineColor":"#38BDF8","secondaryColor":"#2563EB","tertiaryColor":"#0B1220","edgeLabelBackground":"#1E293B","clusterBkg":"#0B1220","clusterBorder":"#38BDF8","titleColor":"#E2E8F0","fontFamily":"Segoe UI, Arial, sans-serif"}}}%%
flowchart TD
    classDef ext fill:#0B1220,stroke:#38BDF8,color:#E2E8F0,stroke-width:2px
    classDef fw fill:#2563EB,stroke:#38BDF8,color:#FFFFFF,stroke-width:2px
    classDef rt fill:#06B6D4,stroke:#0B1220,color:#0B1220,stroke-width:2px
    classDef sw fill:#38BDF8,stroke:#0B1220,color:#0B1220,stroke-width:2px
    classDef host fill:#1E293B,stroke:#38BDF8,color:#E2E8F0
    classDef adm fill:#1E293B,stroke:#06B6D4,color:#E2E8F0,stroke-width:3px
    classDef ok fill:#06B6D4,stroke:#0B1220,color:#0B1220
    classDef bad fill:#1E293B,stroke:#94A3B8,color:#E2E8F0
    classDef step fill:#1E293B,stroke:#38BDF8,color:#E2E8F0
    classDef key fill:#2563EB,stroke:#38BDF8,color:#FFFFFF
    classDef out fill:#0B1220,stroke:#06B6D4,color:#E2E8F0
    A(["▶ --mode remediate"]):::key --> B["Auditoría inicial<br/>informe ANTES"]:::step
    B --> C{"¿Hay controles FAIL<br/>con corrección automática?"}
    C -->|"No"| Z["Nada que remediar"]:::bad
    C -->|"Sí"| D["Mostrar los comandos a aplicar"]:::step
    D --> E{"¿Confirma?<br/>(o --yes)"}
    E -->|"No"| Y["Omitir el equipo"]:::bad
    E -->|"Sí"| F["Enviar los comandos al equipo"]:::key
    F --> G["Guardar la configuración<br/>write memory · FortiOS guarda solo"]:::step
    G --> H["Leer la configuración de nuevo"]:::step
    H --> I["Re-auditar<br/>informe DESPUÉS"]:::step
    I --> J["Informe HTML + JSON<br/>antes vs después"]:::out
    Z --> J
    Y --> J

```

## Documentación por control

Cada ficha incluye identificador, dispositivo, riesgo, recomendación, configuración aplicada, justificación, prueba de validación y resultado antes y después.

| Dispositivo | Ficha | Cumplimiento |
|---|---|---|
| **R1** (router) | [`controles/R1-router.md`](controles/R1-router.md) | 4.3 % → 78.3 % |
| **SW1** (switch) | [`controles/SW1-switch.md`](controles/SW1-switch.md) | 8.3 % → 75.0 % |
| **FW1** (FortiGate) | [`controles/FW1-firewall.md`](controles/FW1-firewall.md) | 30.8 % → 92.3 % |

## Controles que no se automatizan

| Control | Motivo |
|---|---|
| `MGT-03` `enable secret` | Solo se automatiza si se define `CIS_ENABLE_NEW`; no se escriben claves en archivos ni informes. |
| `MGT-05` usuarios con `secret` | El script no conoce la contraseña, por lo que no puede generar el hash. |
| `FGT-14` política ANY-ANY-ALL | Decidir qué tráfico se permite es una decisión de diseño. |
