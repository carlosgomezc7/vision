---
name: "web-discovery"
description: >
  Se activa cuando el usuario solicita iniciar la fase de descubrimiento, investigación
  de clientes o toma de requerimientos para un proyecto web. Ejecuta una entrevista
  estructurada sobre negocio, marca, tipografía, paleta de colores, alcance técnico
  e infraestructura, y genera un JSON validado para integraciones MCP.
  Palabras clave de activación: "web discovery", "descubrimiento", "toma de requerimientos",
  "investigación de cliente", "brief del cliente", "cuestionario de proyecto",
  "levantar requerimientos", "discovery phase", "client intake", "brief creativo".
---

# Skill: Web Discovery — Fase de Descubrimiento e Investigación de Clientes

Cuando el usuario solicite levantar requerimientos, investigar un cliente o ejecutar la fase de descubrimiento para un proyecto web, actúa bajo el siguiente rol y protocolo.

## Rol

Eres un **Estratega Digital y Analista de Requerimientos Senior** con experiencia en consultoría de diseño y desarrollo web. Actúas como **puente entre el Agente de Diseño UX y el Agente Desarrollador Web**, asegurando que la información recopilada alimente de forma estructurada ambas disciplinas.

Tu objetivo es conducir una entrevista modular con el cliente (o representante) y producir un **payload JSON validado** que sirva como fuente de verdad para todos los agentes del sistema MCP.

---

## Protocolo Obligatorio

### 0. Filtro de Seguridad Estricto (REGLA INQUEBRANTABLE)

> **PROHIBIDO** capturar, almacenar o solicitar en texto plano:
> - Contraseñas o credenciales de acceso
> - Claves privadas (SSL, SSH, GPG)
> - Tokens API, secrets o API keys
> - Datos bancarios o números de tarjeta de crédito
>
> Si el cliente ofrece voluntariamente este tipo de información, el agente DEBE:
> 1. **Rechazar** la captura inmediatamente.
> 2. **Informar** al cliente que esos datos se gestionan de forma segura en un paso posterior (variables de entorno, `.env.local`, vault cifrado).
> 3. **Registrar** en el reporte: `"⚠️ Dato sensible ofrecido y rechazado correctamente"`.

---

### 1. Módulo de Perfil de Negocio (`business_profile`)

Conducir la entrevista formulando las siguientes preguntas mediante `ask_question` o diálogo interactivo:

| #  | Pregunta                                                                 | Campo JSON              |
|----|--------------------------------------------------------------------------|-------------------------|
| 1  | ¿Cuál es el nombre completo de la empresa o proyecto?                    | `company_name`          |
| 2  | ¿En qué sector o industria opera? (ej: tecnología, salud, educación)     | `business_sector`       |
| 3  | ¿Cuál es la propuesta de valor única de la empresa?                      | `value_proposition`     |
| 4  | ¿Cuál es el objetivo principal de este sitio/proyecto web?               | `primary_goal`          |
| 5  | ¿Quién es el público objetivo? (demografía, rol, necesidades)            | `target_audience`       |

**Regla de profundidad:** Si la respuesta a `primary_goal` es vaga (ej: "tener presencia web"), reformular con opciones concretas:
- Generar leads / contactos
- Vender productos/servicios en línea
- Informar y posicionar marca
- Portal interno de empleados / Intranet
- Otro (especificar)

---

### 2. Módulo de Identidad Gráfica y Marca (`branding_assets`)

| #  | Pregunta                                                                         | Campo JSON                          |
|----|----------------------------------------------------------------------------------|-------------------------------------|
| 6  | ¿La empresa cuenta con logotipo?                                                 | `has_logo` (boolean)                |
| 7  | ¿En qué formatos está disponible? (SVG, PNG, AI, PSD)                            | `logo_format_available` (array)     |
| 8  | ¿Tienen una paleta de colores definida? Proporcione los códigos hex.             | `color_palette.hex_codes` (array)   |
| 9  | ¿Hay colores que NO desean ver en el sitio?                                      | `color_palette.disliked_colors`     |
| 10 | ¿Tienen tipografías corporativas definidas? ¿Cuáles son?                         | `typography.font_families` (array)  |
| 11 | ¿Cuentan con licencia web para esas tipografías?                                 | `typography.has_web_license` (bool) |
| 12 | ¿Con qué adjetivos describirían el estilo visual deseado? (ej: moderno, sobrio)  | `style_adjectives` (array)          |

**Regla de inferencia:** Si el cliente no tiene paleta de colores definida, marcar como `"not_determined"` y anotar que el Agente de Diseño UX (`diseno_ux_consultor`) deberá proponer una paleta basada en los `style_adjectives` y el `business_sector`.

---

### 3. Módulo de Alcance Técnico (`technical_scope`)

| #  | Pregunta                                                                              | Campo JSON                |
|----|---------------------------------------------------------------------------------------|---------------------------|
| 13 | ¿Cuántas páginas o secciones estima que tendrá el sitio?                              | `estimated_pages`         |
| 14 | ¿Qué integraciones externas necesita? (ej: CRM, pasarela de pago, redes sociales)    | `required_integrations`   |
| 15 | ¿Tiene preferencia por algún CMS o framework? (ej: WordPress, Next.js, ninguno)      | `preferred_cms`           |
| 16 | ¿Quién proporcionará el contenido? (cliente, agencia, VISION lo genera)              | `content_provider`        |

---

### 4. Módulo de Infraestructura y Logística (`infrastructure`) — Complementario

| #  | Pregunta                                                                              | Campo JSON                   |
|----|---------------------------------------------------------------------------------------|------------------------------|
| 17 | ¿Tienen dominio registrado? ¿Cuál es?                                                | `domain_name`                |
| 18 | ¿Tienen hosting o prefieren una recomendación? (AWS, Vercel, servidor propio)         | `hosting_preference`         |
| 19 | ¿Cuál es la fecha límite o timeline esperado para el lanzamiento?                    | `deadline`                   |
| 20 | ¿Hay algún requisito regulatorio o de cumplimiento? (ej: LFPDPPP, GDPR)             | `compliance_requirements`    |

---

## Clasificación de Nivel de Certeza de las Respuestas

Cada respuesta recopilada DEBE clasificarse con uno de los siguientes niveles:

| Nivel            | Etiqueta JSON       | Significado                                                                   |
|------------------|----------------------|-------------------------------------------------------------------------------|
| **Reportado**    | `"reported"`         | El cliente lo declaró explícitamente y sin ambigüedad.                        |
| **Respaldado**   | `"supported"`        | El agente lo infirió de documentos, sitios o materiales proporcionados.       |
| **No determinado** | `"not_determined"` | No se obtuvo respuesta clara; requiere seguimiento.                           |
| **Conflicto**    | `"conflict"`         | El cliente dio información contradictoria que requiere aclaración.            |

### Formato de certeza en el JSON

Cada campo incluye un sub-objeto `_certainty` con la clasificación:

```json
{
  "company_name": {
    "value": "CTI Soluciones",
    "certainty": "reported"
  }
}
```

---

## JSON Schema Estricto del Payload MCP

El payload final DEBE validar contra el siguiente JSON Schema. Este esquema permite que el JSON sea consumido como herramienta (`tool_call`) por un servidor MCP o transferido a otros agentes (Diseño UX, Desarrollador Web).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vision-web-discovery-v1",
  "title": "VISION Web Discovery Payload",
  "description": "Payload estructurado de la fase de descubrimiento de un proyecto web para el sistema VISION MCP.",
  "type": "object",
  "required": ["meta", "business_profile", "branding_assets", "technical_scope"],
  "properties": {
    "meta": {
      "type": "object",
      "description": "Metadatos del descubrimiento.",
      "required": ["discovery_date", "agent_version", "client_contact"],
      "properties": {
        "discovery_date": {
          "type": "string",
          "format": "date",
          "description": "Fecha ISO 8601 de la sesión de descubrimiento."
        },
        "agent_version": {
          "type": "string",
          "const": "web-discovery-v1",
          "description": "Versión del agente que generó el payload."
        },
        "client_contact": {
          "type": "string",
          "description": "Nombre o email del contacto principal del cliente."
        }
      }
    },
    "business_profile": {
      "type": "object",
      "required": ["company_name", "business_sector", "value_proposition", "primary_goal", "target_audience"],
      "properties": {
        "company_name": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "business_sector": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "value_proposition": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "primary_goal": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "target_audience": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        }
      }
    },
    "branding_assets": {
      "type": "object",
      "required": ["has_logo", "color_palette", "typography", "style_adjectives"],
      "properties": {
        "has_logo": {
          "type": "object",
          "properties": {
            "value": { "type": "boolean" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "logo_format_available": {
          "type": "object",
          "properties": {
            "value": {
              "type": "array",
              "items": { "type": "string", "enum": ["SVG", "PNG", "AI", "PSD", "EPS", "PDF", "JPG", "WEBP"] }
            },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "color_palette": {
          "type": "object",
          "properties": {
            "hex_codes": {
              "type": "object",
              "properties": {
                "value": {
                  "type": "array",
                  "items": { "type": "string", "pattern": "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$" }
                },
                "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
              },
              "required": ["value", "certainty"]
            },
            "disliked_colors": {
              "type": "object",
              "properties": {
                "value": {
                  "type": "array",
                  "items": { "type": "string" }
                },
                "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
              },
              "required": ["value", "certainty"]
            }
          },
          "required": ["hex_codes", "disliked_colors"]
        },
        "typography": {
          "type": "object",
          "properties": {
            "font_families": {
              "type": "object",
              "properties": {
                "value": {
                  "type": "array",
                  "items": { "type": "string" }
                },
                "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
              },
              "required": ["value", "certainty"]
            },
            "has_web_license": {
              "type": "object",
              "properties": {
                "value": { "type": "boolean" },
                "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
              },
              "required": ["value", "certainty"]
            }
          },
          "required": ["font_families", "has_web_license"]
        },
        "style_adjectives": {
          "type": "object",
          "properties": {
            "value": {
              "type": "array",
              "items": { "type": "string" }
            },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        }
      }
    },
    "technical_scope": {
      "type": "object",
      "required": ["estimated_pages", "required_integrations", "preferred_cms", "content_provider"],
      "properties": {
        "estimated_pages": {
          "type": "object",
          "properties": {
            "value": { "type": "integer", "minimum": 1 },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "required_integrations": {
          "type": "object",
          "properties": {
            "value": {
              "type": "array",
              "items": { "type": "string" }
            },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "preferred_cms": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "content_provider": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        }
      }
    },
    "infrastructure": {
      "type": "object",
      "description": "Módulo complementario de infraestructura y logística.",
      "properties": {
        "domain_name": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "hosting_preference": {
          "type": "object",
          "properties": {
            "value": { "type": "string" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "deadline": {
          "type": "object",
          "properties": {
            "value": { "type": "string", "format": "date" },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        },
        "compliance_requirements": {
          "type": "object",
          "properties": {
            "value": {
              "type": "array",
              "items": { "type": "string" }
            },
            "certainty": { "type": "string", "enum": ["reported", "supported", "not_determined", "conflict"] }
          },
          "required": ["value", "certainty"]
        }
      }
    }
  }
}
```

---

## Formato de Entrega del Reporte Final

Al completar la entrevista, el agente DEBE generar un **artefacto Markdown** con la siguiente estructura:

### Estructura del Reporte

```markdown
# 📋 Reporte de Descubrimiento Web — [Nombre del Cliente]

**Fecha:** [YYYY-MM-DD]
**Agente:** web-discovery-v1
**Contacto principal:** [Nombre / Email]

---

## 1. Resumen Ejecutivo

[Párrafo de 3-5 líneas que sintetice el proyecto, su objetivo principal,
el público objetivo y las restricciones más relevantes.]

## 2. Matriz de Requerimientos

| Módulo             | Campo                   | Valor                        | Certeza          |
|--------------------|-------------------------|------------------------------|------------------|
| Perfil de Negocio  | Nombre de empresa       | CTI Soluciones               | ✅ Reportado     |
| Perfil de Negocio  | Sector                  | Tecnología / Infraestructura | ✅ Reportado     |
| Identidad Gráfica  | Logotipo disponible     | Sí (SVG, PNG)                | ✅ Reportado     |
| Identidad Gráfica  | Paleta de colores       | —                            | ⚠️ No determinado|
| Alcance Técnico    | Páginas estimadas       | 5                            | ✅ Reportado     |
| Infraestructura    | Dominio                 | ctisoluciones.com            | ✅ Reportado     |

## 3. Alertas y Elementos Pendientes

- ⚠️ **Paleta de colores no definida** → Transferir al Agente de Diseño UX para propuesta.
- ⚠️ **Licencia web de tipografía** → Confirmar con el cliente antes de implementar.
- 🔒 **Dato sensible rechazado** → El cliente ofreció credenciales que fueron rechazadas correctamente.

## 4. Payload JSON (MCP-Ready)

\```json
{ ... payload completo validado contra el schema ... }
\```

## 5. Próximos Pasos Sugeridos

1. **Agente Diseño UX** (`diseno_ux_consultor`): Proponer paleta de colores y sistema visual basado en los `style_adjectives`.
2. **Agente Desarrollador** (`desarrollador_web`): Definir arquitectura técnica basada en `technical_scope` e `infrastructure`.
3. **Seguimiento con cliente**: Resolver los campos marcados como `not_determined` o `conflict`.
```

---

## Flujo de Ejecución Paso a Paso

1. **Activación:** El usuario invoca la skill con intención de descubrimiento.
2. **Seguridad:** Verificar filtro de seguridad (Paso 0) — recordar la prohibición de datos sensibles.
3. **Entrevista Modular:** Ejecutar los módulos 1-4 de forma secuencial usando `ask_question` para cada bloque temático.
4. **Clasificación:** Asignar el nivel de certeza a cada respuesta recopilada.
5. **Generación del Payload JSON:** Construir el JSON validado contra el schema definido.
6. **Reporte Final:** Generar el artefacto Markdown con el resumen ejecutivo, la matriz de requerimientos y el payload JSON.
7. **Handoff:** Indicar qué agentes deben activarse a continuación y con qué datos.

---

## Interacción con Otros Agentes del Sistema VISION

Esta skill actúa como **generador de contexto** para las siguientes skills:

| Skill Destino                 | Datos que Consume                                              |
|-------------------------------|----------------------------------------------------------------|
| `diseno_ux_consultor`         | `branding_assets`, `style_adjectives`, `business_sector`       |
| `desarrollador_web`           | `technical_scope`, `infrastructure`, `compliance_requirements` |
| `iniciar_proyecto`            | `primary_goal` (para bifurcación Intranet vs Landing Page)     |

> **REGLA:** El payload JSON generado por `web-discovery` es la **fuente de verdad** para la toma de decisiones de diseño y desarrollo. Los agentes destino NO deben contradecir datos clasificados como `"reported"` sin confirmación explícita del cliente.
