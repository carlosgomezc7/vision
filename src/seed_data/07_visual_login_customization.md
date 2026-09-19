# Visual Customization Guide — Login per Client

This document defines which files are customized per client and the design guidelines. The functionality (auth, middleware, server actions) is NEVER modified.

## Files Customizable per Client

| File | What is customized |
|------|--------------------|
| `src/app/globals.css` | Color palette, animations, visual effects |
| `src/app/login/page.tsx` | Login layout, logo, texts, taglines |
| `src/app/dashboard/page.tsx` | Post-login design, visible modules |
| `src/app/layout.tsx` | Metadata (title, description, language) |

## Login Elements Adapted per Client

### 1. Color Palette
Change CSS variables in `globals.css`:
- `--primary`: Main brand color
- Hero panel gradients
- Floating orb colors
- Primary button color

### 2. Logo and Branding
In `login/page.tsx`:
- SVG icon or client's logo image
- Company name
- Custom tagline

### 3. Texts and Copy
- Hero title ("Your Smart Intranet" → customize)
- Hero description
- Feature pills (e.g.: "Deep Search AI", "Secure RBAC")
- Footer with client's copyright

### 4. Visual Effects (optional)
- Background animation type (orbs, particles, gradients)
- Glassmorphism intensity
- Animation speed

## Default Base Design (Template)

The default template uses a **modern elegant blue** style with:

- **Layout**: Split screen (60% hero / 40% form)
- **Background**: `#080e1a` (deep night blue)
- **Hero**: Gradient `#0a1628` → `#0f2847` → `#1a3a6b`
- **Accents**: `#2563eb`, `#3b82f6`, `#60a5fa`
- **Effects**: Glassmorphism, floating orbs, shimmer on hover
- **Form**: Email + Password with visibility toggle + Login/Signup toggle
- **Animations**: Staggered entrance (slide-up with delays)
- **Responsive**: Stacks vertically on mobile

## Authentication Flow (DO NOT modify)

```
/ (root) → [no session] → /login
/ (root) → [with session] → /dashboard
/login → [successful login] → /dashboard
/login → [signup] → confirm email → /login
/dashboard → [logout] → /login
```

## How to Create a New Intranet Project

1. Follow the steps in `05_blueprint_login_setup.md`
2. Copy the standard code from `06_reusable_auth_code.md`
3. Customize files marked as 🎨 CUSTOMIZABLE
4. Create Supabase project and configure `.env.local`
5. Enable Email provider in Supabase → Authentication → Providers
