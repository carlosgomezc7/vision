# Guía de Personalización Visual — Login por Cliente

Este documento define qué archivos se personalizan por cliente y las pautas de diseño. La funcionalidad (auth, middleware, server actions) NUNCA se modifica.

## Archivos Personalizables por Cliente

| Archivo | Qué se personaliza |
|---------|-------------------|
| `src/app/globals.css` | Paleta de colores, animaciones, efectos visuales |
| `src/app/login/page.tsx` | Layout del login, logo, textos, taglines |
| `src/app/dashboard/page.tsx` | Diseño post-login, módulos visibles |
| `src/app/layout.tsx` | Metadata (título, descripción, idioma) |

## Elementos del Login que se Adaptan por Cliente

### 1. Paleta de Colores
Cambiar las variables CSS en `globals.css`:
- `--primary`: Color principal de marca
- Gradientes del hero panel
- Colores de orbes flotantes
- Color del botón principal

### 2. Logo y Branding
En `login/page.tsx`:
- Ícono SVG o imagen del logo del cliente
- Nombre de la empresa
- Tagline personalizado

### 3. Textos y Copy
- Título del hero ("Tu Intranet Inteligente" → personalizar)
- Descripción del hero
- Feature pills (ej: "Deep Search IA", "RBAC Seguro")
- Footer con copyright del cliente

### 4. Efectos Visuales (opcionales)
- Tipo de animaciones de fondo (orbes, partículas, gradientes)
- Intensidad del glassmorphism
- Velocidad de animaciones

## Diseño Base Estándar (Template Default)

El template default usa un estilo **azul moderno elegante** con:

- **Layout**: Split screen (60% hero / 40% formulario)
- **Fondo**: `#080e1a` (azul noche profundo)
- **Hero**: Gradiente `#0a1628` → `#0f2847` → `#1a3a6b`
- **Acentos**: `#2563eb`, `#3b82f6`, `#60a5fa`
- **Efectos**: Glassmorphism, orbes flotantes, shimmer en hover
- **Formulario**: Email + Password con toggle visibilidad + Login/Signup toggle
- **Animaciones**: Entrada escalonada (slide-up con delays)
- **Responsive**: En mobile se apila verticalmente

## Flujo de Autenticación (NO modificar)

```
/ (raíz) → [sin sesión] → /login
/ (raíz) → [con sesión] → /dashboard
/login → [login exitoso] → /dashboard
/login → [signup] → confirma email → /login
/dashboard → [logout] → /login
```

## Cómo Crear un Nuevo Proyecto de Intranet

1. Seguir los pasos de `05_blueprint_login_setup.md`
2. Copiar el código estándar de `06_codigo_auth_reutilizable.md`
3. Personalizar los archivos marcados como 🎨 PERSONALIZABLE
4. Crear proyecto Supabase y configurar `.env.local`
5. Habilitar Email provider en Supabase → Authentication → Providers
