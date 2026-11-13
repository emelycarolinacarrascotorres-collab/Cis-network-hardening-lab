# 🛡️ Controles CIS · R1 (router)

[🏠 README](../../README.md) · [📘 Hardening](../04-hardening.md) · [📊 Resultados](../06-resultados.md)

---

**Auditoría inicial:** 4.3 % (1/23 controles) &nbsp;→&nbsp; **Auditoría final:** 78.3 % (18/23 controles)

Fuentes: [`reports/auditoria-inicial`](../../reports/auditoria-inicial) · [`reports/auditoria-final`](../../reports/auditoria-final) · configuración: [`configs/router/R1-antes.cfg`](../../configs/router/R1-antes.cfg) → [`configs/router/R1-despues.cfg`](../../configs/router/R1-despues.cfg)

> **Leyenda:** ✅ cumple · ❌ no cumple · 🟡 requiere acción manual · ⚪ no evaluable. Los comandos listados son los que genera el script a partir de la configuración *antes*; el resultado real lo determina la auditoría final.

## Resumen

| ID | Control | Antes | Después | Estado |
|---|---|:---:|:---:|---|
| `MGT-01` | Habilitar 'aaa new-model' | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-02` | Definir 'aaa authentication login default' | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-03` | Usar 'enable secret' (sin 'enable password') | 🟡 MANUAL | 🟡 MANUAL | Pendiente (manual) |
| `MGT-04` | Habilitar 'service password-encryption' | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-05` | Usuarios locales con 'secret' (no 'password') | 🟡 MANUAL | 🟡 MANUAL | Pendiente (manual) |
| `MGT-06` | exec-timeout <= 10 min en consola | ❌ FAIL | ❌ FAIL | Aplicado · el script lo marca FAIL (falso negativo) |
| `MGT-07` | exec-timeout <= 10 min en VTY | ❌ FAIL | ❌ FAIL | Aplicado · el script lo marca FAIL (falso negativo) |
| `MGT-08` | 'transport input ssh' en VTY | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-09` | ACL de acceso (access-class) en VTY | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-10` | Configurar 'banner login' | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-11` | Eliminar SNMP communities 'public'/'private' | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-12` | Deshabilitar servidor HTTP ('no ip http server') | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-13` | SSH versión 2 | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-14` | 'ip ssh time-out' <= 60 s | ❌ FAIL | ✅ PASS | **Remediado** |
| `MGT-15` | 'ip ssh authentication-retries' <= 3 | ❌ FAIL | ❌ FAIL | Aplicado · el script lo marca FAIL (falso negativo) |
| `CTL-01` | Deshabilitar CDP ('no cdp run') | ❌ FAIL | ✅ PASS | **Remediado** |
| `CTL-02` | 'no ip bootp server' | ❌ FAIL | ✅ PASS | **Remediado** |
| `CTL-03` | 'no service pad' | ❌ FAIL | ✅ PASS | **Remediado** |
| `CTL-04` | 'logging buffered' >= 16384 | ❌ FAIL | ✅ PASS | **Remediado** |
| `CTL-05` | Enviar logs a servidor syslog | ❌ FAIL | ✅ PASS | **Remediado** |
| `CTL-06` | Timestamps con fecha/hora en logs y debug | ✅ PASS | ✅ PASS | Ya cumplía |
| `DAT-01` | 'no ip source-route' | ❌ FAIL | ✅ PASS | **Remediado** |
| `DAT-02` | 'no ip proxy-arp' en interfaces L3 | ❌ FAIL | ✅ PASS | **Remediado** |

## Detalle por control

*(Haga clic en cada control para desplegarlo.)*

<details>
<summary><b><code>MGT-01</code></b> · Habilitar 'aaa new-model' &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-01` · Ref. CIS: 1.1.1
- **Dispositivo:** R1 (router)
- **Riesgo:** Sin AAA no hay listas de métodos de autenticación ni base para trazabilidad y control centralizados.
- **Recomendación:** Habilitar 'aaa new-model'
- **Justificación:** Activa AAA: base para autenticación por listas de métodos y trazabilidad de accesos.
- **Prueba de validación:** `show running-config | include aaa new-model` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
aaa new-model
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L19: no aaa new-model
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L22: aaa new-model
```

</details>

<details>
<summary><b><code>MGT-02</code></b> · Definir 'aaa authentication login default' &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-02` · Ref. CIS: 1.1.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Consola y VTY quedan protegidas solo por contraseñas de línea, sin método de autenticación explícito.
- **Recomendación:** Definir 'aaa authentication login default'
- **Justificación:** Obliga a que consola y VTY usen un método de autenticación explícito (local) en vez de contraseñas de línea.
- **Prueba de validación:** `show running-config | include aaa authentication` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
aaa authentication login default local
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L25: aaa authentication login default local
```

</details>

<details>
<summary><b><code>MGT-03</code></b> · Usar 'enable secret' (sin 'enable password') &nbsp; 🟡 → 🟡</summary>

- **Identificador:** `MGT-03` · Ref. CIS: 1.4.1
- **Dispositivo:** R1 (router)
- **Riesgo:** `enable password` es reversible o texto claro: quien vea la configuración obtiene el acceso privilegiado.
- **Recomendación:** Usar 'enable secret' (sin 'enable password')
- **Justificación:** El modo privilegiado debe protegerse con hash fuerte (scrypt) y no con una contraseña reversible.
- **Prueba de validación:** `show running-config | include ^enable` · Prueba n.º 7 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [tipo 7](../../evidence/06-pruebas/04-snmp-password-r1.png)
- **Resultado antes:** 🟡 `MANUAL` — Existe 'enable password' (reversible / texto claro) -> requiere acción manual
- **Resultado después:** 🟡 `MANUAL` — Existe 'enable password' (reversible / texto claro) -> requiere acción manual
- **Estado:** Pendiente (manual)

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L17: enable password <REDACTED>
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L20: enable password <REDACTED>
```

🟡 Pendiente (manual). Confirmado en el equipo: sigue `enable password` con cifrado **tipo 7 (reversible)**. Procedimiento: `enable algorithm-type scrypt secret <clave>` y `no enable password`.

</details>

<details>
<summary><b><code>MGT-04</code></b> · Habilitar 'service password-encryption' &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-04` · Ref. CIS: 1.4.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Las contraseñas de línea quedan visibles en texto claro al mostrar la configuración.
- **Recomendación:** Habilitar 'service password-encryption'
- **Justificación:** Evita que contraseñas de línea aparezcan en texto claro al ver la configuración (mitigación básica).
- **Prueba de validación:** `show running-config | include password-encryption` · Prueba n.º 7 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [password-encryption](../../evidence/06-pruebas/04-snmp-password-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
service password-encryption
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L11: service password-encryption
```

</details>

<details>
<summary><b><code>MGT-05</code></b> · Usuarios locales con 'secret' (no 'password') &nbsp; 🟡 → 🟡</summary>

- **Identificador:** `MGT-05` · Ref. CIS: 1.4.3
- **Dispositivo:** R1 (router)
- **Riesgo:** Credenciales de usuarios locales almacenadas con `password` (reversibles) en lugar de un hash.
- **Recomendación:** Usuarios locales con 'secret' (no 'password')
- **Justificación:** Un hash fuerte protege las credenciales locales si se filtra la configuración. Requiere acción manual (no se conoce la clave).
- **Prueba de validación:** `show running-config | include ^username` · Evidencia: [tipo 7](../../evidence/06-pruebas/04-snmp-password-r1.png)
- **Resultado antes:** 🟡 `MANUAL` — Usuarios sin 'secret': admin -> requiere acción manual
- **Resultado después:** 🟡 `MANUAL` — Usuarios sin 'secret': admin -> requiere acción manual
- **Estado:** Pendiente (manual)

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L41: username admin privilege 15 password 0 <REDACTED>
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L55: username admin privilege 15 password 7 <REDACTED>
```

🟡 Pendiente (manual). Confirmado en el equipo: el usuario local sigue con `password 7` (reversible). Procedimiento: `username admin privilege 15 secret <clave>` y `no username admin password`.

</details>

<details>
<summary><b><code>MGT-06</code></b> · exec-timeout <= 10 min en consola &nbsp; ❌ → ❌</summary>

- **Identificador:** `MGT-06` · Ref. CIS: 1.2.7
- **Dispositivo:** R1 (router)
- **Riesgo:** Una consola desatendida con sesión privilegiada abierta (`exec-timeout 0 0` = nunca expira) permite acceso físico oportunista.
- **Recomendación:** exec-timeout <= 10 min en consola
- **Justificación:** Cierra sesiones de consola abandonadas; reduce el riesgo de acceso físico oportunista.
- **Prueba de validación:** `show running-config all | section line con 0` · Prueba n.º 6 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [show line con 0](../../evidence/06-pruebas/07-show-line-con0-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple: line con 0
- **Resultado después:** ❌ `FAIL` — No cumple: line con 0
- **Estado:** Aplicado · el script lo marca FAIL (falso negativo)

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
line con 0
 exec-timeout 10 0
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L97: line con 0
L98:  exec-timeout 0 0
L99:  privilege level 15
L100:  logging synchronous
L101:  stopbits 1
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L123: line con 0
L124:  privilege level 15
L125:  logging synchronous
L126:  stopbits 1
```

✅ **Falso negativo confirmado en el equipo.** `show line con 0` indica *Idle EXEC 00:10:00* ([captura](../../evidence/06-pruebas/07-show-line-con0-r1.png)). El valor coincide con el valor *por defecto* de IOS, que no se muestra en `show running-config`; el script interpreta la ausencia de la línea como incumplimiento. Ver también la evidencia *después* de la configuración: la línea no aparece.

Observación: `line aux 0` conserva `exec-timeout 0 0` (no está entre los controles seleccionados).

</details>

<details>
<summary><b><code>MGT-07</code></b> · exec-timeout <= 10 min en VTY &nbsp; ❌ → ❌</summary>

- **Identificador:** `MGT-07` · Ref. CIS: 1.2.8
- **Dispositivo:** R1 (router)
- **Riesgo:** Las sesiones remotas inactivas permanecen abiertas y pueden secuestrarse.
- **Recomendación:** exec-timeout <= 10 min en VTY
- **Justificación:** Cierra sesiones remotas inactivas; reduce la ventana para secuestro de sesión.
- **Prueba de validación:** `show running-config all | section line vty`  ·  comprobar el cierre por inactividad · Prueba n.º 6 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [show line vty 0](../../evidence/06-pruebas/07-show-line-vty-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple: line vty 0 4; line vty 5 15
- **Resultado después:** ❌ `FAIL` — No cumple: line vty 0 4; line vty 5 15
- **Estado:** Aplicado · el script lo marca FAIL (falso negativo)

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
line vty 0 4
 exec-timeout 10 0
line vty 5 15
 exec-timeout 10 0
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L107: line vty 0 4
L108:  login local
L109:  transport input all
L110: line vty 5 15
L111:  login local
L112:  transport input all
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L132: line vty 0 4
L133:  access-class CIS-VTY-ACL in
L134:  transport input ssh
L135: line vty 5 15
L136:  access-class CIS-VTY-ACL in
L137:  transport input ssh
```

✅ **Falso negativo confirmado en el equipo.** `show line vty 0` indica *Idle EXEC 00:10:00* ([captura](../../evidence/06-pruebas/07-show-line-vty-r1.png)). El valor coincide con el valor *por defecto* de IOS, que no se muestra en `show running-config`; el script interpreta la ausencia de la línea como incumplimiento. Ver también la evidencia *después* de la configuración: la línea no aparece.

</details>

<details>
<summary><b><code>MGT-08</code></b> · 'transport input ssh' en VTY &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-08` · Ref. CIS: 1.2.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Telnet transmite usuario y contraseña en texto claro; un sniffer en el segmento las captura.
- **Recomendación:** 'transport input ssh' en VTY
- **Justificación:** Telnet envía credenciales en claro; solo se permite SSH (cifrado).
- **Prueba de validación:** `telnet <IP>` debe ser rechazado; `show running-config | section line vty` · Prueba n.º 1, 5 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [puerto 23 cerrado](../../evidence/06-pruebas/01-telnet-puerto23-cerrado-r1.png), [show line vty 0](../../evidence/06-pruebas/07-show-line-vty-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple: line vty 0 4; line vty 5 15
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
line vty 0 4
 transport input ssh
line vty 5 15
 transport input ssh
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L107: line vty 0 4
L108:  login local
L109:  transport input all
L110: line vty 5 15
L111:  login local
L112:  transport input all
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L132: line vty 0 4
L133:  access-class CIS-VTY-ACL in
L134:  transport input ssh
L135: line vty 5 15
L136:  access-class CIS-VTY-ACL in
L137:  transport input ssh
```

</details>

<details>
<summary><b><code>MGT-09</code></b> · ACL de acceso (access-class) en VTY &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-09` · Ref. CIS: 1.2.4 / 1.2.5
- **Dispositivo:** R1 (router)
- **Riesgo:** Cualquier red con ruta al equipo puede intentar autenticarse (fuerza bruta, abuso de credenciales).
- **Recomendación:** ACL de acceso (access-class) en VTY
- **Justificación:** Solo la red de gestión puede intentar conectarse por SSH al dispositivo (reduce superficie de ataque).
- **Prueba de validación:** SSH desde un host fuera de la VLAN 99 debe fallar; `show access-lists CIS-VTY-ACL` · Prueba n.º 2, 3 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple: line vty 0 4; line vty 5 15
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
ip access-list standard CIS-VTY-ACL
 permit 10.25.20.0 0.0.0.255
 deny any log
line vty 0 4
 access-class CIS-VTY-ACL in
line vty 5 15
 access-class CIS-VTY-ACL in
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L107: line vty 0 4
L108:  login local
L109:  transport input all
L110: line vty 5 15
L111:  login local
L112:  transport input all
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L132: line vty 0 4
L133:  access-class CIS-VTY-ACL in
L134:  transport input ssh
L135: line vty 5 15
L136:  access-class CIS-VTY-ACL in
L137:  transport input ssh
```

</details>

<details>
<summary><b><code>MGT-10</code></b> · Configurar 'banner login' &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-10` · Ref. CIS: 1.3.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Sin aviso legal es más difícil sustentar acciones contra accesos no autorizados.
- **Recomendación:** Configurar 'banner login'
- **Justificación:** Aviso legal de acceso autorizado: base legal para sancionar accesos no autorizados.
- **Prueba de validación:** Conectar al equipo y verificar que aparece el aviso · Prueba n.º 3 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
banner login #AUTHORIZED ACCESS ONLY. Activity is monitored and logged. Disconnect immediately if you are not an authorized user.#
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L121: banner login ^CAUTHORIZED ACCESS ONLY. Activity is monitored and logged. Disconnect immediately if you are not an authorized user.^C
```

</details>

<details>
<summary><b><code>MGT-11</code></b> · Eliminar SNMP communities 'public'/'private' &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-11` · Ref. CIS: 1.5.2 / 1.5.3
- **Dispositivo:** R1 (router)
- **Riesgo:** `public` y `private` son las primeras cadenas que prueba un atacante; `private` (RW) permite modificar el equipo.
- **Recomendación:** Eliminar SNMP communities 'public'/'private'
- **Justificación:** Son las primeras cadenas que prueba cualquier atacante; 'private' (RW) permite modificar el equipo.
- **Prueba de validación:** `show running-config | include snmp-server`  ·  consulta SNMP con `public` sin respuesta · Prueba n.º 4 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [sin communities](../../evidence/06-pruebas/04-snmp-password-r1.png)
- **Resultado antes:** ❌ `FAIL` — Communities por defecto: public, private
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no snmp-server community public
no snmp-server community private
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L90: snmp-server community public RO
L91: snmp-server community private RW
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
(sin líneas relacionadas)
```

</details>

<details>
<summary><b><code>MGT-12</code></b> · Deshabilitar servidor HTTP ('no ip http server') &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-12` · Ref. CIS: 2.1.x
- **Dispositivo:** R1 (router)
- **Riesgo:** El servidor HTTP administra sin cifrar y amplía la superficie de ataque.
- **Recomendación:** Deshabilitar servidor HTTP ('no ip http server')
- **Justificación:** HTTP es texto claro y expande la superficie de ataque; la gestión se hace por SSH.
- **Prueba de validación:** `Test-NetConnection <IP> -Port 80` debe dar `False` · Prueba n.º 5 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [puerto 80 cerrado](../../evidence/06-pruebas/05-http-cerrado-r1-sw1.png)
- **Resultado antes:** ❌ `FAIL` — 'ip http server' activo
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no ip http server
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L85: ip http server
L86: no ip http secure-server
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L105: no ip http server
L106: no ip http secure-server
```

</details>

<details>
<summary><b><code>MGT-13</code></b> · SSH versión 2 &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-13` · Ref. CIS: 2.1.1.x
- **Dispositivo:** R1 (router)
- **Riesgo:** SSH versión 1 tiene debilidades criptográficas conocidas.
- **Recomendación:** SSH versión 2
- **Justificación:** SSHv1 tiene debilidades criptográficas conocidas.
- **Prueba de validación:** `show ip ssh` (versión 2.0) · Evidencia: [show ip ssh](../../evidence/06-pruebas/07-show-ip-ssh-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
ip ssh version 2
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L62: ip ssh time-out 60
L63: ip ssh version 2
```

</details>

<details>
<summary><b><code>MGT-14</code></b> · 'ip ssh time-out' <= 60 s &nbsp; ❌ → ✅</summary>

- **Identificador:** `MGT-14` · Ref. CIS: 2.1.1.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Conexiones SSH que no terminan de autenticarse consumen líneas VTY (denegación de servicio).
- **Recomendación:** 'ip ssh time-out' <= 60 s
- **Justificación:** Limita el tiempo para completar la autenticación SSH (mitiga conexiones colgadas / DoS).
- **Prueba de validación:** `show ip ssh` · Evidencia: [show ip ssh](../../evidence/06-pruebas/07-show-ip-ssh-r1.png)
- **Resultado antes:** ❌ `FAIL` — Debe ser <= 60 (no configurado)
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
ip ssh time-out 60
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L62: ip ssh time-out 60
```

</details>

<details>
<summary><b><code>MGT-15</code></b> · 'ip ssh authentication-retries' <= 3 &nbsp; ❌ → ❌</summary>

- **Identificador:** `MGT-15` · Ref. CIS: 2.1.1.3
- **Dispositivo:** R1 (router)
- **Riesgo:** Intentos de contraseña ilimitados por sesión facilitan la fuerza bruta.
- **Recomendación:** 'ip ssh authentication-retries' <= 3
- **Justificación:** Limita intentos de contraseña por sesión SSH (mitiga fuerza bruta).
- **Prueba de validación:** `show ip ssh`  ·  `show running-config all | include authentication-retries` · Evidencia: [show ip ssh](../../evidence/06-pruebas/07-show-ip-ssh-r1.png)
- **Resultado antes:** ❌ `FAIL` — Debe ser <= 3 (no configurado)
- **Resultado después:** ❌ `FAIL` — Debe ser <= 3 (no configurado)
- **Estado:** Aplicado · el script lo marca FAIL (falso negativo)

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
ip ssh authentication-retries 3
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
(sin líneas relacionadas)
```

✅ **Falso negativo confirmado en el equipo.** `show ip ssh` indica *Authentication retries: 3* ([captura](../../evidence/06-pruebas/07-show-ip-ssh-r1.png)). El valor coincide con el valor *por defecto* de IOS, que no se muestra en `show running-config`; el script interpreta la ausencia de la línea como incumplimiento. Ver también la evidencia *después* de la configuración: la línea no aparece.

</details>

<details>
<summary><b><code>CTL-01</code></b> · Deshabilitar CDP ('no cdp run') &nbsp; ❌ → ✅</summary>

- **Identificador:** `CTL-01` · Ref. CIS: 2.1.2
- **Dispositivo:** R1 (router)
- **Riesgo:** CDP revela modelo, versión de IOS e IPs a cualquier vecino de capa 2 (reconocimiento).
- **Recomendación:** Deshabilitar CDP ('no cdp run')
- **Justificación:** CDP revela modelo, IOS e IPs a cualquier vecino L2 (reconocimiento).
- **Prueba de validación:** `show cdp neighbors` → `CDP is not enabled` · Prueba n.º 8 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: [show cdp neighbors](../../evidence/06-pruebas/06-cdp-r1.png)
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no cdp run
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L114: no cdp run
```

</details>

<details>
<summary><b><code>CTL-02</code></b> · 'no ip bootp server' &nbsp; ❌ → ✅</summary>

- **Identificador:** `CTL-02` · Ref. CIS: 2.1.3
- **Dispositivo:** R1 (router)
- **Riesgo:** BOOTP es un servicio heredado, sin uso, que expone el equipo.
- **Recomendación:** 'no ip bootp server'
- **Justificación:** Servicio innecesario que expone el equipo a abuso/descarga de configuración.
- **Prueba de validación:** `show running-config | include bootp` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no ip bootp server
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L40: no ip bootp server
```

</details>

<details>
<summary><b><code>CTL-03</code></b> · 'no service pad' &nbsp; ❌ → ✅</summary>

- **Identificador:** `CTL-03` · Ref. CIS: 2.1.8
- **Dispositivo:** R1 (router)
- **Riesgo:** PAD (X.25) es un servicio heredado que amplía la superficie de ataque.
- **Recomendación:** 'no service pad'
- **Justificación:** PAD (X.25) es un servicio heredado y sin uso; se elimina para reducir superficie.
- **Prueba de validación:** `show running-config | include service pad` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no service pad
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L8: no service pad
```

</details>

<details>
<summary><b><code>CTL-04</code></b> · 'logging buffered' >= 16384 &nbsp; ❌ → ✅</summary>

- **Identificador:** `CTL-04` · Ref. CIS: 2.2.2
- **Dispositivo:** R1 (router)
- **Riesgo:** Un buffer pequeño pierde eventos antes de poder analizarlos.
- **Recomendación:** 'logging buffered' >= 16384
- **Justificación:** Un buffer mayor conserva eventos para análisis forense local.
- **Prueba de validación:** `show logging | include Log Buffer` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — Debe ser >= 16384 (no configurado)
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
logging buffered 64000
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L19: logging buffered 64000
```

</details>

<details>
<summary><b><code>CTL-05</code></b> · Enviar logs a servidor syslog &nbsp; ❌ → ✅</summary>

- **Identificador:** `CTL-05` · Ref. CIS: 2.2.4
- **Dispositivo:** R1 (router)
- **Riesgo:** Los logs solo locales se pierden al reiniciar o si el equipo se compromete.
- **Recomendación:** Enviar logs a servidor syslog
- **Justificación:** Logs centralizados no se pierden si el equipo se reinicia o es comprometido.
- **Prueba de validación:** `show logging | include logging to` · Prueba n.º 9 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
logging host 10.25.20.10
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L113: logging host 10.25.20.10
```

</details>

<details>
<summary><b><code>CTL-06</code></b> · Timestamps con fecha/hora en logs y debug &nbsp; ✅ → ✅</summary>

- **Identificador:** `CTL-06` · Ref. CIS: 2.2.6
- **Dispositivo:** R1 (router)
- **Riesgo:** Eventos sin fecha y hora no pueden correlacionarse durante un incidente.
- **Recomendación:** Timestamps con fecha/hora en logs y debug
- **Justificación:** Sin marca de tiempo no se pueden correlacionar eventos durante un incidente.
- **Prueba de validación:** `show running-config | include timestamps` · Prueba n.º 9 de [`05-pruebas.md`](../05-pruebas.md) · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ✅ `PASS`
- **Resultado después:** ✅ `PASS`
- **Estado:** Ya cumplía

**Configuración aplicada:** ninguna; el control ya se cumplía antes del hardening.

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`:

```text
L8: service timestamps debug datetime msec
L9: service timestamps log datetime msec
```

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L9: service timestamps debug datetime msec
L10: service timestamps log datetime msec
```

</details>

<details>
<summary><b><code>DAT-01</code></b> · 'no ip source-route' &nbsp; ❌ → ✅</summary>

- **Identificador:** `DAT-01` · Ref. CIS: 3.1.1
- **Dispositivo:** R1 (router)
- **Riesgo:** El origen del paquete puede dictar su ruta y evadir controles de seguridad.
- **Recomendación:** 'no ip source-route'
- **Justificación:** Impide que el origen dicte la ruta del paquete (técnica usada para evadir controles).
- **Prueba de validación:** `show running-config | include source-route` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
no ip source-route
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L32: no ip source-route
```

</details>

<details>
<summary><b><code>DAT-02</code></b> · 'no ip proxy-arp' en interfaces L3 &nbsp; ❌ → ✅</summary>

- **Identificador:** `DAT-02` · Ref. CIS: 3.1.x
- **Dispositivo:** R1 (router)
- **Riesgo:** El router responde ARP en nombre de otros hosts: facilita suplantación y fuga entre segmentos.
- **Recomendación:** 'no ip proxy-arp' en interfaces L3
- **Justificación:** Evita que el router responda ARP por otros hosts (suplantación / fuga entre segmentos).
- **Prueba de validación:** `show running-config interface <IF> | include proxy-arp` · Evidencia: **[AGREGAR CAPTURA]**
- **Resultado antes:** ❌ `FAIL` — No cumple: interface GigabitEthernet1/0; interface GigabitEthernet2/0.10; interface GigabitEthernet2/0.20; interface GigabitEthernet2/0.99
- **Resultado después:** ✅ `PASS`
- **Estado:** **Remediado**

**Configuración aplicada (comandos que genera el script a partir de la configuración *antes*):**

```text
interface GigabitEthernet1/0
 no ip proxy-arp
interface GigabitEthernet2/0.10
 no ip proxy-arp
interface GigabitEthernet2/0.20
 no ip proxy-arp
interface GigabitEthernet2/0.99
 no ip proxy-arp
```

**Evidencia en la configuración (antes)** — `configs/router/R1-antes.cfg`: el parámetro no aparece (no está configurado).

**Evidencia en la configuración (después)** — `configs/router/R1-despues.cfg`:

```text
L80: no ip proxy-arp
L90: no ip proxy-arp
L95: no ip proxy-arp
L100: no ip proxy-arp
```

</details>
