---
name: "Iniciar Proyecto de Intranet"
description: >
  Se activa cuando el usuario dice frases como: "vamos a comenzar un proyecto",
  "iniciemos un proyecto", "hey vision iniciemos un proyecto", "nuevo proyecto",
  "crea un proyecto", "arranquemos un proyecto", "quiero un nuevo proyecto",
  "empecemos un proyecto", "comencemos", "inicia un proyecto", "start a project",
  "new project", o cualquier variación que combine un saludo o mención a VISION
  con la intención de iniciar/crear/arrancar un proyecto nuevo de intranet.
---

# Skill: Generador de Proyectos Web de VISION

Cuando el usuario invoque a **VISION** para crear un proyecto ("iniciemos un proyecto", "crea un proyecto", "landing page", "sitio web", "intranet", etc.), sigue este flujo **OBLIGATORIO** antes de escribir código:

## Paso 1: Pregunta Primaria Obligatoria de VISION

Lo **PRIMERO** que debe preguntar VISION mediante `ask_question` son las **2 opciones fundamentales**:

1. **¿Qué tipo de proyecto deseas crear?**:
   - `Opción 1: Intranet Corporativa B2B (con Auth, Supabase, RBAC y Dashboard)`
   - `Opción 2: Landing Page / One Page / Página Web Estática (sin Auth ni Supabase)`
2. **Nombre del cliente / proyecto** (ej: "Grupo Alfa", "CTI Soluciones")
3. **Ruta del proyecto en el filesystem** (ej: `/home/carlos/Documents/grupo-alfa`)
4. **¿Inicializar repositorio Git?** (Sí / No)

---

## BIFURCACIÓN A: Sitio Web Público / Landing Page Estática

Si el usuario elige **Sitio Web Público / Landing Page**:

### A.1 NO instalar Supabase ni crear carpetas de Autenticación
No crear `src/lib/supabase/`, ni `src/app/login/`, ni `src/app/dashboard/`, ni `middleware.ts`.

### A.2 Preguntar detalles de Contenido y Diseño
Realizar las siguientes preguntas (o usar `ask_question` / diálogo interactivo):
1. **Páginas / Secciones requeridas** (Inicio, Servicios, Nosotros, Contacto).
2. **Contenido de cada sección**:
   - **Inicio**: Eslogan principal, llamada a la acción (CTA).
   - **Servicios**: Lista de servicios clave y descripciones.
   - **Nosotros**: Historia, misión o propuesta de valor.
   - **Contacto**: Datos de contacto (correo, teléfono, dirección, formulario).
3. **Estilo Visual y Colores**: Paleta de colores preferida (tonos oscuros/claros, azul corporativo, verde, etc.).
4. **Imágenes y Recursos Visuales**:
   - ¿El cliente proporciona imágenes propias?
   - Si no las proporciona, generarlas autónomamente con `generate_image` o usar componentes gráficos modernos en React.

### A.3 Crear la estructura Next.js pura
```bash
mkdir -p <ruta-del-proyecto>
cd <ruta-del-proyecto>
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes
```

### A.4 Instalar dependencias visuales (Lucide icons, shadcn UI)
```bash
npx -y shadcn@latest init --yes --defaults --force
npm install lucide-react
```

### A.5 Construir la experiencia limpia y verificar
- Implementar la estructura navegable (Inicio, Servicios, Nosotros, Contacto) sin dependencias a backend ni base de datos.
- **REGLA DE ARQUITECTURA FRONTEND (LANDING PAGE):** La página principal NUNCA debe ser un solo archivo gigante (`src/app/page.tsx`). Debe modularizarse por secciones en la carpeta `src/components/landing/` (ej. `Header.tsx`, `Hero.tsx`, `Services.tsx`, `Contact.tsx`, `Footer.tsx`) y luego importarse en `page.tsx`. Conservar el diseño de botones superiores.
- Ejecutar `npm run build` y `npm run dev`.

---

## BIFURCACIÓN B: Intranet Corporativa B2B (con Auth Supabase)

Si el usuario elige **Intranet Corporativa (B2B con Auth)**:

### B.1 Crear directorio e inicializar Next.js
```bash
mkdir -p <ruta-del-proyecto>
cd <ruta-del-proyecto>
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes
```

### B.2 Instalar dependencias estándar
```bash
npx -y shadcn@latest init --yes --defaults --force
npm install @supabase/supabase-js @supabase/ssr lucide-react
```

### B.3 Copiar código funcional estándar de Auth
Crear:
- `src/lib/supabase/client.ts`
- `src/lib/supabase/server.ts`
- `src/lib/supabase/middleware.ts`
- `src/middleware.ts`
- `src/app/login/actions.ts`
- `src/app/login/page.tsx`
- `src/app/dashboard/page.tsx`
- `.env.local.example`

### B.4 Solicitar credenciales Supabase y verificar
- Configurar `.env.local`
- Ejecutar `npm run build` y `npm run dev`

