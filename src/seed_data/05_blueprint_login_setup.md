# Blueprint: Login para Intranet B2B — Setup Base

Este documento describe los pasos exactos para crear el módulo de login de cualquier Intranet B2B de CTI Soluciones. La funcionalidad es estándar y reutilizable; solo el diseño visual se personaliza por cliente.

## 1. Inicialización del Proyecto

```bash
# Crear proyecto Next.js con App Router + TypeScript + Tailwind
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes

# Inicializar Shadcn UI
npx -y shadcn@latest init --yes --defaults --force

# Instalar Supabase
npm install @supabase/supabase-js @supabase/ssr
```

## 2. Estructura de Archivos (estándar para todos los proyectos)

```
intranet/
├── .env.local                    # Credenciales Supabase (por proyecto)
├── .env.local.example            # Template sin credenciales
├── src/
│   ├── app/
│   │   ├── layout.tsx            # Layout raíz (metadata por cliente)
│   │   ├── page.tsx              # Redirect según auth
│   │   ├── globals.css           # 🎨 PERSONALIZABLE por cliente
│   │   ├── login/
│   │   │   ├── page.tsx          # 🎨 PERSONALIZABLE (diseño visual)
│   │   │   └── actions.ts       # ✅ ESTÁNDAR (no modificar)
│   │   └── dashboard/
│   │       └── page.tsx          # 🎨 PERSONALIZABLE
│   ├── lib/
│   │   └── supabase/
│   │       ├── client.ts         # ✅ ESTÁNDAR (no modificar)
│   │       ├── server.ts         # ✅ ESTÁNDAR (no modificar)
│   │       └── middleware.ts     # ✅ ESTÁNDAR (no modificar)
│   └── middleware.ts             # ✅ ESTÁNDAR (no modificar)
```

## 3. Variables de Entorno

Archivo `.env.local` (credenciales únicas por proyecto Supabase):
```
NEXT_PUBLIC_SUPABASE_URL=<url-del-proyecto-supabase>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon-key-del-proyecto-supabase>
```

Se obtienen desde: Supabase Dashboard → Settings → API.

## 4. Requisito en Supabase

Habilitar el proveedor **Email** en: Authentication → Providers → Email.
A futuro se pueden agregar SSO (Microsoft 365, Google Workspace, Okta) sin modificar la estructura base.
