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

# Skill: Iniciar Proyecto de Intranet B2B

Cuando el usuario indique que quiere iniciar un nuevo proyecto, sigue este flujo **OBLIGATORIO** antes de escribir cualquier línea de código:

## Paso 1: Preguntar información del proyecto

Usa la herramienta `ask_question` para solicitar:

1. **Tipo de proyecto** — Sitio Web Público (Landing Page/Corporativo) vs Intranet Corporativa (B2B con Auth)
2. **Nombre del cliente** — Este será el nombre del proyecto (ej: "Grupo Alfa", "Corporativo Beta")
3. **Ruta del proyecto** — Dónde crear el proyecto en el filesystem (ej: `/home/carlos/Documents/grupo-alfa`)
4. **¿Inicializar repositorio Git?** — Sí / No

## Paso 2: Crear el proyecto

Una vez que el usuario responda, ejecuta estos pasos en orden:

### 2.1 Crear directorio e inicializar Next.js
```bash
mkdir -p <ruta-del-proyecto>
cd <ruta-del-proyecto>
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes
```

### 2.2 Instalar dependencias estándar
```bash
npx -y shadcn@latest init --yes --defaults --force
npm install @supabase/supabase-js @supabase/ssr
```

### 2.3 Copiar código funcional estándar

Consulta la memoria de VISION (documento `06_codigo_auth_reutilizable.md`) y crea estos archivos **exactamente como están documentados** (NO se modifican por cliente):

- `src/lib/supabase/client.ts`
- `src/lib/supabase/server.ts`
- `src/lib/supabase/middleware.ts`
- `src/middleware.ts`
- `src/app/login/actions.ts`
- `src/app/page.tsx`
- `.env.local.example`

### 2.4 Crear archivos personalizables

Consulta la memoria de VISION (documento `07_personalizacion_visual_login.md`) y crea versiones personalizadas con el nombre del cliente:

- `src/app/globals.css` — Preguntar estilo de color preferido
- `src/app/login/page.tsx` — Con el logo y nombre del cliente
- `src/app/dashboard/page.tsx` — Con branding del cliente
- `src/app/layout.tsx` — Con metadata del cliente

### 2.5 Inicializar Git (si el usuario lo solicitó)
```bash
git init
git add .
git commit -m "feat: setup inicial intranet <nombre-cliente>"
```

## Paso 3: Solicitar credenciales de Supabase

Preguntar al usuario por las credenciales:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

Crear `.env.local` con los valores proporcionados.

## Paso 4: Verificar

- Ejecutar `npm run build` para verificar que todo compila.
- Ejecutar `npm run dev` para levantar el servidor.
- Confirmar al usuario que el proyecto está listo.
