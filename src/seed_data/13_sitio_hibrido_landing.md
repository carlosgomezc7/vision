# Sitio Híbrido: Landing Page Pública + Intranet Privada

## Decisión de Producto (2026-08-02)
El usuario eligió el modelo **Sitio Híbrido** donde la ruta `/` es una página pública de servicios y `/dashboard` es la Intranet privada protegida por autenticación.

## Estructura de Rutas
| Ruta | Tipo | Descripción |
|------|------|-------------|
| `/` | Pública | Landing Page de servicios de CTI Soluciones (Hero, Servicios, Contacto, Footer) |
| `/login` | Pública | Pantalla de inicio de sesión / registro con diseño Glassmorphism |
| `/dashboard` | Protegida | Portal interno de la Intranet (solo usuarios autenticados) |

## Middleware de Protección
El archivo `src/lib/supabase/middleware.ts` fue modificado para:
- Permitir acceso libre a `/` y `/login` (rutas públicas).
- Redirigir usuarios no autenticados que intenten acceder a `/dashboard` → `/login`.
- Redirigir usuarios ya autenticados que visiten `/login` → `/dashboard`.

## Landing Page (src/app/page.tsx)
Secciones implementadas:
1. **Header Sticky** con navegación (Inicio, Servicios, Nosotros, Contacto) y botón "Acceder a Intranet".
2. **Sección Hero** con métricas (99.9% uptime, Deep Search IA, ISO/IEC, 24/7 Soporte).
3. **Portafolio de Servicios** (3 tarjetas: Intranets IA, Software a la Medida, Cloud & Ciberseguridad).
4. **Banner de Integración** con la Intranet para clientes existentes.
5. **Formulario de Contacto** interactivo con simulación de envío.
6. **Footer** con enlaces y copyright dinámico.

## Problema de Puerto Fantasma (Issue #2)
Al reiniciar el servidor de desarrollo, una instancia anterior ocupaba el puerto 3000. El nuevo servidor arrancó silenciosamente en 3001, mostrando una versión desactualizada. Se resolvió matando el proceso huérfano con `kill -9`.
