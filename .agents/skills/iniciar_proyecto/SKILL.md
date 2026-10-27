---
name: "Iniciar Proyecto de Landing Page"
description: >
  Se activa cuando el usuario dice frases como: "vamos a comenzar un proyecto",
  "iniciemos un proyecto", "hey vision iniciemos un proyecto", "nuevo proyecto",
  "crea un proyecto", "arranquemos un proyecto", "quiero un nuevo proyecto",
  "empecemos un proyecto", "comencemos", "inicia un proyecto", "start a project",
  "new project", "crear landing page", o cualquier variación para arrancar una
  Landing Page o Sitio Web personalizado.
---

# Skill: Generador de Landing Pages Personalizadas de VISION

Cuando el usuario invoque a **VISION** para crear una Landing Page o sitio web ("iniciemos un proyecto", "crea un proyecto", "nueva landing page", etc.), sigue este flujo centrado en **darle prioridad al cliente y escuchar lo que busca**:

---

## Paso 1: Escucha al Cliente y Preguntas Clave

Usa `ask_question` o diálogo interactivo para capturar:

1. **Nombre del cliente / empresa** (ej: "Grupo Alfa", "Café La Sierra").
2. **Propuesta de valor y objetivo principal** (ej: "¿Qué problema resuelves y cuál es la acción principal deseada: WhatsApp, formulario o llamada?").
3. **Estilo visual y referencias** (ej: minimalista, elegante, corporativo, cálido; URLs o marcas que le gusten al cliente).
4. **Paleta de colores** (códigos hex corporativos o colores que el cliente NO desea ver).
5. **Ruta del proyecto en el filesystem** (ej: `/home/carlos/Projects/grupo-alfa`).

---

## Paso 2: Auditoría de Preparación (`audit_client_readiness_score`)

Antes de escribir código:
- Ejecuta `audit_client_readiness_score(payload)`.
- Si el puntaje es menor a 80%, presenta las preguntas de seguimiento al cliente para no adivinar nada.
- Ejecuta `generate_design_tokens_w3c` y `audit_theme_palette` para asegurar contraste WCAG 2.2 AA (4.5:1).

---

## Paso 3: Inicializar Next.js Limpio y Modular

```bash
mkdir -p <ruta-del-proyecto>
cd <ruta-del-proyecto>
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes
npx -y shadcn@latest init --yes --defaults --force
npm install lucide-react
```

---

## Paso 4: Arquitectura Modular por Secciones

**REGLA DE ARQUITECTURA FRONTEND:**
La página principal NUNCA debe ser un solo archivo gigante (`src/app/page.tsx`). Debe modularizarse por secciones independientes bajo `src/components/landing/`:
- `Header.tsx` (Logo, navegación suave y CTA superior)
- `Hero.tsx` (Titular llamativo, propuesta de valor y botón principal)
- `Services.tsx` o `Features.tsx` (Tarjetas de servicios con iconos Lucide)
- `About.tsx` (Historia o credenciales de la empresa)
- `Testimonials.tsx` (Prueba social)
- `Contact.tsx` (Botón directo a WhatsApp, formulario y datos de contacto)
- `Footer.tsx` (Pie de página accesible)

`src/app/page.tsx` únicamente importa y orquesta estas secciones.

---

## Paso 5: Verificación y Entrega

1. Ejecutar `npm run build` para asegurar cero errores de TypeScript y compilación estática.
2. Auditar accesibilidad por teclado y contraste con `check_wcag_accessibility`.
3. Iniciar servidor de desarrollo con `npm run dev`.
