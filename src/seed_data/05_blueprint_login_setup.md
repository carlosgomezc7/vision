# Blueprint: B2B Intranet Login — Base Setup

This document describes the exact steps to create the login module for any B2B Intranet by CTI Soluciones. The functionality is standard and reusable; only the visual design is customized per client.

## 1. Project Initialization

```bash
# Create Next.js project with App Router + TypeScript + Tailwind
npx -y create-next-app@latest ./ --typescript --tailwind --eslint --app --src-dir --import-alias "@/*" --use-npm --yes

# Initialize Shadcn UI
npx -y shadcn@latest init --yes --defaults --force

# Install Supabase
npm install @supabase/supabase-js @supabase/ssr
```

## 2. File Structure (standard for all projects)

```
intranet/
├── .env.local                    # Supabase credentials (per project)
├── .env.local.example            # Template without credentials
├── src/
│   ├── app/
│   │   ├── layout.tsx            # Root layout (metadata per client)
│   │   ├── page.tsx              # Redirect based on auth
│   │   ├── globals.css           # 🎨 CUSTOMIZABLE per client
│   │   ├── login/
│   │   │   ├── page.tsx          # 🎨 CUSTOMIZABLE (visual design)
│   │   │   └── actions.ts       # ✅ STANDARD (do not modify)
│   │   └── dashboard/
│   │       └── page.tsx          # 🎨 CUSTOMIZABLE
│   ├── lib/
│   │   └── supabase/
│   │       ├── client.ts         # ✅ STANDARD (do not modify)
│   │       ├── server.ts         # ✅ STANDARD (do not modify)
│   │       └── middleware.ts     # ✅ STANDARD (do not modify)
│   └── middleware.ts             # ✅ STANDARD (do not modify)
```

## 3. Environment Variables

File `.env.local` (unique credentials per Supabase project):
```
NEXT_PUBLIC_SUPABASE_URL=<supabase-project-url>
NEXT_PUBLIC_SUPABASE_ANON_KEY=<supabase-anon-key>
```

Obtained from: Supabase Dashboard → Settings → API.

## 4. Supabase Requirement

Enable the **Email** provider at: Authentication → Providers → Email.
SSO providers (Microsoft 365, Google Workspace, Okta) can be added in the future without modifying the base structure.
