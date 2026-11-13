[🏠 Inicio](../README.md) · [◀ Propósito](01-proposito.md) · [Configuración ▶](03-configuracion.md)

# 🏗️ 02 · Topología

---

<div align="center">
<img src="../assets/images/topologia-gns3.png" alt="Topología del laboratorio en GNS3" width="85%"/>

*Topología real en GNS3.*
</div>

## Diagrama de red

```mermaid
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#1E293B","primaryTextColor":"#E2E8F0","primaryBorderColor":"#38BDF8","lineColor":"#38BDF8","secondaryColor":"#2563EB","tertiaryColor":"#0B1220","edgeLabelBackground":"#1E293B","clusterBkg":"#0B1220","clusterBorder":"#38BDF8","titleColor":"#E2E8F0","fontFamily":"Segoe UI, Arial, sans-serif"}}}%%
flowchart LR
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
    NAT(["☁️ NAT1<br/>salida a Internet"]):::ext
    FW["🔥 FW1 · FortiGate 7.0.9<br/>port1 (DHCP, hacia NAT1)<br/>port2 10.25.0.2/30"]:::fw
    R1["🌐 R1 · Router<br/>Gi1/0 10.25.0.1/30<br/>Gi2/0 trunk 802.1Q"]:::rt
    SW["🔀 SW1 · Switch IOSv L2 15.2<br/>Gi0/0 trunk<br/>Vlan99 10.25.20.2"]:::sw

    NAT --- FW
    FW ---|"10.25.0.0/30"| R1
    R1 ---|"trunk VLAN 10 / 20 / 99"| SW

    subgraph V10["VLAN 10 · USUARIOS · 10.25.6.0/24 · GW 10.25.6.1"]
        PCU["💻 PC-User<br/>10.25.6.10"]:::host
    end
    subgraph V20["VLAN 20 · SERVIDORES · 10.25.97.0/24 · GW 10.25.97.1"]
        SRV["🖥️ Servidor web<br/>web-server-lab-1"]:::host
    end
    subgraph V99["VLAN 99 · GESTIÓN · 10.25.20.0/24 · GW 10.25.20.1"]
        ADM["🛡️ PC-Admin · Windows 10<br/>10.25.20.10<br/>ejecuta cis_hardening.py"]:::adm
    end

    SW ---|"Gi0/1"| PCU
    SW ---|"Gi0/2"| SRV
    SW ---|"Gi0/3"| ADM

```

## Dispositivos

| Nodo en GNS3 | Rol | Sistema | Gestión |
|---|---|---|---|
| `NAT1` | Salida a Internet | Nodo NAT de GNS3 | — |
| `FortiGate7.0.9-1` (hostname `FW1`) | Firewall | FortiOS 7.0.9 (VM64-KVM) | 10.25.0.2 |
| `R1` | Router | Cisco IOS 15.2 | 10.25.20.1 |
| `CiscoIOSvL215.2(20200924:215240)-1` (hostname `SW1`) | Switch capa 2 | Cisco IOSv L2 15.2 | 10.25.20.2 |
| `windows10-1` / `Cloneofwindows10-1` | PC-Admin y PC-User | Windows 10 | 10.25.20.10 (PC-Admin) · 10.25.6.10 (PC-User) |
| `web-server-lab-1` | Servidor web | Servidor de GNS3 | VLAN 20 · IP: **[AGREGAR]** |

PC-User verificado con `ipconfig`: IP `10.25.6.10`, gateway `10.25.6.1` ([captura](../evidence/06-pruebas/13-fw-trusthost-pc-user-timeout.png)).

> **[AGREGAR]** cuál de los dos nodos Windows de GNS3 es PC-Admin y cuál PC-User.

## Direccionamiento

| VLAN | Nombre | Red | Gateway (R1) |
|---|---|---|---|
| 10 | USUARIOS | 10.25.6.0/24 | 10.25.6.1 (`Gi2/0.10`) |
| 20 | SERVIDORES | 10.25.97.0/24 | 10.25.97.1 (`Gi2/0.20`) |
| 99 | GESTIÓN | 10.25.20.0/24 | 10.25.20.1 (`Gi2/0.99`) |
| — | Enlace R1 ↔ FW1 | 10.25.0.0/30 | R1 `Gi1/0` 10.25.0.1 · FW1 `port2` 10.25.0.2 |

Ruta por defecto de R1: `0.0.0.0/0` vía `10.25.0.2` (FW1). El direccionamiento se derivó de la matrícula **2025-0697**.

## Interfaces

| Equipo | Interfaz | Función |
|---|---|---|
| R1 | `Gi1/0` 10.25.0.1/30 | Enlace hacia FW1 |
| R1 | `Gi2/0` (troncal 802.1Q) | Subinterfaces `.10`, `.20` y `.99` |
| R1 | `Fa0/0` | Apagada (*shutdown*) |
| SW1 | `Gi0/0` | Troncal hacia R1 |
| SW1 | `Gi0/1` · `Gi0/2` · `Gi0/3` | Acceso VLAN 10 · 20 · 99 |
| SW1 | `Vlan99` 10.25.20.2/24 | Gestión (gateway `10.25.20.1`) |
| FW1 | `port2` 10.25.0.2/30 | Enlace hacia R1 |
| FW1 | `port1` (DHCP) | Salida hacia NAT1 **[VERIFICAR]** |

Fuente: [`configs/`](../configs) y [capturas](../evidence/02-configuracion).

## Flujo de administración tras el hardening *(resultado esperado)*

```mermaid
%%{init: {"theme":"base","themeVariables":{"primaryColor":"#1E293B","primaryTextColor":"#E2E8F0","primaryBorderColor":"#38BDF8","lineColor":"#38BDF8","secondaryColor":"#2563EB","tertiaryColor":"#0B1220","edgeLabelBackground":"#1E293B","clusterBkg":"#0B1220","clusterBorder":"#38BDF8","titleColor":"#E2E8F0","fontFamily":"Segoe UI, Arial, sans-serif"}}}%%
sequenceDiagram
    autonumber
    participant ADM as PC-Admin (VLAN 99)
    participant USR as PC-User (VLAN 10)
    participant R1 as R1 (VTY + ACL)
    ADM->>R1: SSH a 10.25.20.1
    R1-->>ADM: Permitido (origen en la red de gestión)
    USR->>R1: SSH a 10.25.20.1
    R1--xUSR: Denegado por la ACL de las líneas VTY
    USR->>R1: Telnet o SNMP con community por defecto
    R1--xUSR: Rechazado

```

> Describe el **resultado esperado**; las pruebas que lo comprueban están en [05-pruebas.md](05-pruebas.md).
