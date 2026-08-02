# Protocolo de Inicio de Proyecto — Trigger Automático

## Frases que Activan el Protocolo

Cualquier frase que combine la intención de "iniciar/crear/comenzar un proyecto" activa el flujo de creación de Intranet. Ejemplos:

- "Vamos a comenzar un proyecto"
- "Hey VISION, iniciemos un proyecto"
- "Nuevo proyecto"
- "Crea un proyecto"
- "Arranquemos un proyecto"
- "Quiero un nuevo proyecto"
- "Empecemos un proyecto"
- "Comencemos"
- "Inicia un proyecto"
- "Start a project"
- "New project"
- Cualquier variación con saludo + intención de nuevo proyecto

## Flujo Obligatorio al Detectar el Trigger

### 1. PREGUNTAR antes de crear

Solicitar al usuario:
1. **Nombre del cliente** (será el nombre del proyecto, ej: "Grupo Alfa")
2. **Ruta del proyecto** (dónde crearlo en el filesystem)
3. **¿Inicializar repositorio Git?** (Sí / No)

### 2. CREAR con base estándar

- Inicializar Next.js + Tailwind + Shadcn + Supabase (ver `05_blueprint_login_setup.md`)
- Copiar código funcional estándar SIN modificar (ver `06_codigo_auth_reutilizable.md`)
- Personalizar archivos visuales con branding del cliente (ver `07_personalizacion_visual_login.md`)
- Preguntar estilo de color preferido para el diseño

### 3. CONFIGURAR credenciales

- Solicitar URL y Anon Key de Supabase
- Crear `.env.local`
- Verificar build y levantar servidor

## Regla Clave

La funcionalidad (auth, middleware, server actions) es IDÉNTICA en todos los proyectos. Solo cambia:
- Nombre/logo del cliente
- Paleta de colores y estilo visual
- Textos y taglines del hero
- Credenciales de Supabase (.env.local)
