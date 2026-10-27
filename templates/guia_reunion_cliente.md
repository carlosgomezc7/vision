# 🎯 Guía de Escucha al Cliente para Landing Pages Personalizadas
*CTI Soluciones — Carlos Gómez*

Esta guía está diseñada para que en tus reuniones con clientes te enfoques al **100% en escucharlos**, entender su negocio y capturar sus gustos estéticos sin preocuparte por tecnicismos ni código. Al terminar la plática, cada dato responderá a una necesidad exacta de tu repositorio **VISION MCP**.

---

## 🗺️ Matriz: Qué Escuchar del Cliente vs. Qué Necesita el Repo

| # | Qué preguntarle / escuchar del cliente | Qué busca descubrir tu oído | En qué campo se guarda | Qué herramienta de VISION lo consume | Resultado tangible generado |
|---|---|---|---|---|---|
| **1** | *"¿Cómo se llama tu marca y qué problema resuelves mejor que nadie?"* | Nombre oficial y propuesta de valor única. | `nombre_empresa`<br>`propuesta_de_valor`<br>`sector_industria` | `create_landing_page_specification` | Título SEO, OpenGraph, copy del Hero y propósito central de la Landing. |
| **2** | *"¿Qué es lo más importante que quieres que haga la persona al entrar a la página?"* | Objetivo de conversión directo (CTA). | `objetivo_principal_landing`<br>`llamado_a_la_accion_cta` | `create_landing_page_specification`<br>`audit_performance_budget` | Botón principal de llamada a la acción (WhatsApp, formulario, llamada, agenda). |
| **3** | *"¿Qué sitios web te gustan o admiras? ¿Qué estilo visual imaginas?"* | Gusto estético del cliente (minimalista, elegante, audaz, sobrio, etc.). | `adjetivos_estilo_visual`<br>`sitios_de_referencia_que_le_gustan` | `generate_design_tokens_w3c`<br>`create_landing_page_specification` | Dirección visual, ritmo visual y componentes `shadcn/ui` adecuados. |
| **4** | *"¿Cuentas con colores de marca o hay algún color que NO quieras ver jamás?"* | Paleta base y restricciones de marca. | `paleta_de_colores.colores_deseados_hex`<br>`colores_prohibidos_o_no_deseados` | `audit_theme_palette`<br>`export_tokens_to_stylesheet`<br>`check_wcag_accessibility` | Variables CSS (`:root`) con contraste estricto **WCAG 2.2 AA (4.5:1 / 3.0:1)**. |
| **5** | *"¿Qué secciones consideras indispensables mostrar?"* | Estructura modular del contenido. | `secciones_requeridas` | `create_landing_page_specification` | Creación de componentes modulares bajo `src/components/landing/*.tsx`. |
| **6** | *"¿Por qué medio prefieres que te contacten tus clientes?"* | Canales directos de conversión. | `canales_de_contacto`<br>`redes_sociales` | `create_landing_page_specification` | Componentes de Contacto, botón flotante de WhatsApp y pie de página accesible. |
| **7** | *"¿Cuentas ya con dominio o fotografías propias?"* | Insumos gráficos e infraestructura. | `tiene_logotipo`<br>`recursos_fotograficos`<br>`dominio` | `audit_client_readiness` | Diagnóstico de preparación (Readiness Score %) y siguientes pasos. |

---

## ⚡ Flujo en 3 Pasos con VISION MCP

### Paso 1: Escuchar y recopilar
Durante la reunión, anota libremente o completa [client_discovery_template.json](file:///home/carlosgomezc7/Projects/vision/templates/client_discovery_template.json).

### Paso 2: Ejecutar el Diagnóstico de Preparación
Pásale el JSON a VISION mediante la herramienta:
```python
audit_client_readiness(payload)
```
VISION te entregará:
- **Índice de Preparación (`readiness_score`: 0–100%)**.
- **Qué falta para el repo (`missing_for_repo`)**.
- **Preguntas listas en español para enviar por WhatsApp o correo (`next_questions_for_client`)**.

### Paso 3: Generar la Landing Page 100% Personalizada
Cuando el puntaje sea óptimo, VISION ejecuta automáticamente:
1. `generate_design_tokens_w3c` + `audit_theme_palette` (Tokens accesibles WCAG 2.2).
2. `export_tokens_to_stylesheet` (Generación de CSS / Tailwind).
3. `create_landing_page_specification` (Arquitectura Next.js modular por secciones).
