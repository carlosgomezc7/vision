# Hybrid Site: Public Landing Page + Private Intranet

## Product Decision (2026-08-02)
The user chose the **Hybrid Site** model where the `/` route is a public services page and `/dashboard` is the private intranet protected by authentication.

## Route Structure
| Route | Type | Description |
|-------|------|-------------|
| `/` | Public | CTI Soluciones services Landing Page (Hero, Services, Contact, Footer) |
| `/login` | Public | Login / registration screen with Glassmorphism design |
| `/dashboard` | Protected | Internal Intranet portal (authenticated users only) |

## Protection Middleware
The file `src/lib/supabase/middleware.ts` was modified to:
- Allow free access to `/` and `/login` (public routes).
- Redirect unauthenticated users who try to access `/dashboard` → `/login`.
- Redirect already-authenticated users who visit `/login` → `/dashboard`.

## Landing Page (src/app/page.tsx)
Implemented sections:
1. **Sticky Header** with navigation (Home, Services, About Us, Contact) and "Access Intranet" button.
2. **Hero Section** with metrics (99.9% uptime, Deep Search AI, ISO/IEC, 24/7 Support).
3. **Services Portfolio** (3 cards: AI Intranets, Custom Software, Cloud & Cybersecurity).
4. **Integration Banner** with the Intranet for existing clients.
5. **Interactive Contact Form** with send simulation.
6. **Footer** with links and dynamic copyright.

## Ghost Port Problem (Issue #2)
When restarting the development server, a previous instance occupied port 3000. The new server started silently on 3001, showing an outdated version. Resolved by killing the orphan process with `kill -9`.
