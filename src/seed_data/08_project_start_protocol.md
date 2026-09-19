# Project Start Protocol — Automatic Trigger

## Phrases That Activate the Protocol

Any phrase combining the intent to "start/create/begin a project" activates the Intranet creation flow. Examples:

- "Let's start a project"
- "Hey VISION, let's start a project"
- "New project"
- "Create a project"
- "Let's kick off a project"
- "I want a new project"
- "Let's begin a project"
- "Let's get started"
- "Start a project"
- "New project"
- Any variation with a greeting + new project intent

## Mandatory Flow Upon Detecting the Trigger

### 1. ASK before creating

Request from the user:
1. **Client name** (will be the project name, e.g.: "Grupo Alfa")
2. **Project path** (where to create it on the filesystem)
3. **Initialize Git repository?** (Yes / No)

### 2. CREATE with standard base

- Initialize Next.js + Tailwind + Shadcn + Supabase (see `05_blueprint_login_setup.md`)
- Copy standard functional code WITHOUT modifying (see `06_reusable_auth_code.md`)
- Customize visual files with client branding (see `07_visual_login_customization.md`)
- Ask for preferred color style for the design

### 3. CONFIGURE credentials

- Request Supabase URL and Anon Key
- Create `.env.local`
- Verify build and start server

## Key Rule

The functionality (auth, middleware, server actions) is IDENTICAL across all projects. Only these change:
- Client name/logo
- Color palette and visual style
- Hero texts and taglines
- Supabase credentials (.env.local)
