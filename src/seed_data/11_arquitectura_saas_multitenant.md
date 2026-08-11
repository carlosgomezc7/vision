# Arquitectura SaaS Multi-Tenant — Intranet CTI Soluciones

## Decisión Arquitectónica (2026-08-02)
El proyecto ha evolucionado de una Intranet de empresa única a un modelo **SaaS Multi-Tenant** donde múltiples empresas clientes se registran, obtienen 30 días de prueba y configuran su portal privado.

## Modelo de Datos (Supabase/PostgreSQL)
Las tablas creadas con Row Level Security (RLS) son:
- **organizations**: Empresas registradas (name, logo_url, trial_start_date, is_active).
- **profiles**: Usuarios vinculados a una organización con rol (admin/employee). Extiende auth.users.
- **announcements**: Comunicados corporativos por organización.
- **documents**: Archivos/formatos descargables por organización (Supabase Storage).
- **time_off_requests**: Solicitudes de vacaciones con estados (pending/approved/rejected).

## Aislamiento de Datos (RLS)
Se creó la función `get_user_org_id()` que obtiene el `organization_id` del usuario autenticado. Todas las políticas RLS filtran por esta función, garantizando que la Empresa A nunca vea datos de la Empresa B.

## Flujo de Onboarding
1. Usuario se registra en `/login` → Supabase crea auth.user → Trigger `handle_new_user` crea un row en `profiles` con rol 'admin'.
2. El código de `actions.ts` crea automáticamente una `organization` y vincula al perfil del nuevo usuario.
3. El usuario es redirigido a `/dashboard` donde puede configurar su empresa.

## Tipos de Producto (Selector de Servicio)
Cada organización puede elegir entre 3 modalidades:
1. **Página de Presentación**: Landing page pública de servicios solamente.
2. **Intranet**: Portal privado corporativo con módulos internos (anuncios, vacaciones, documentos).
3. **Híbrido**: Combinación de ambos — Landing pública + Intranet privada.
