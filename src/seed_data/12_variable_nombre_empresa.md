# Configuración Centralizada de Empresa (siteConfig)

## Problema Resuelto (2026-08-02)
Se necesitaba una forma de que el nombre de la empresa ("CTI Soluciones") se propagara automáticamente por toda la aplicación sin tener que editar cada archivo manualmente.

## Solución Implementada
Se creó el archivo `src/lib/config.ts` con un objeto exportado `siteConfig`:

```typescript
export const siteConfig = {
  name: process.env.NEXT_PUBLIC_COMPANY_NAME || "CTI Soluciones",
  shortName: "CTI Soluciones",
  tagline: "Transformación Digital & Soluciones Tecnológicas de Alto Impacto",
  description: "Impulsamos el crecimiento corporativo...",
  contactEmail: "contacto@ctisoluciones.com",
  contactPhone: "+52 (55) 1234-5678",
  address: "Ciudad de México, México",
  services: [...],
};
```

## Dos Niveles de Memoria
1. **Memoria Global (siteConfig):** Variable estática leída por Landing Page, Login, Dashboard y Layout. Se cambia en un solo lugar.
2. **Memoria de Usuario (Supabase):** El Dashboard lee `user.user_metadata?.company_name` como fallback dinámico por usuario. Preparado para Multi-Tenant.

## Archivos que Consumen siteConfig
- `src/app/page.tsx` (Landing Page pública)
- `src/app/login/page.tsx` (Pantalla de Login)
- `src/app/dashboard/page.tsx` (Bienvenida dinámica)
- `src/app/layout.tsx` (Metadatos SEO globales)
