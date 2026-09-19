# Centralized Company Configuration (siteConfig)

## Problem Solved (2026-08-02)
A way was needed for the company name ("CTI Soluciones") to propagate automatically throughout the entire application without having to edit each file manually.

## Implemented Solution
The file `src/lib/config.ts` was created with an exported `siteConfig` object:

```typescript
export const siteConfig = {
  name: process.env.NEXT_PUBLIC_COMPANY_NAME || "CTI Soluciones",
  shortName: "CTI Soluciones",
  tagline: "Digital Transformation & High-Impact Technology Solutions",
  description: "We drive corporate growth...",
  contactEmail: "contact@ctisoluciones.com",
  contactPhone: "+52 (55) 1234-5678",
  address: "Mexico City, Mexico",
  services: [...],
};
```

## Two Levels of Memory
1. **Global Memory (siteConfig):** Static variable read by Landing Page, Login, Dashboard, and Layout. Changed in a single place.
2. **User Memory (Supabase):** The Dashboard reads `user.user_metadata?.company_name` as a dynamic per-user fallback. Ready for Multi-Tenant.

## Files that Consume siteConfig
- `src/app/page.tsx` (Public Landing Page)
- `src/app/login/page.tsx` (Login Screen)
- `src/app/dashboard/page.tsx` (Dynamic welcome)
- `src/app/layout.tsx` (Global SEO metadata)
