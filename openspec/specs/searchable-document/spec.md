## Purpose

Define el contenido indexable (noticias, procedimientos, políticas) que el motor de Deep Search puede procesar y recuperar considerando metadatos y permisos.

## Requirements

### Requirement: Indexación de documentos
El sistema SHALL extraer y almacenar metadatos (título, propietario, etiquetas, fecha) y contenido de los documentos para permitir búsquedas semánticas y por palabras clave.

#### Scenario: Nuevo documento es publicado
- **WHEN** un documento es creado o actualizado en la intranet
- **THEN** el sistema indexa automáticamente su contenido y actualiza los metadatos de búsqueda asociados

### Requirement: Filtrado de búsqueda por permisos
El motor de búsqueda SHALL garantizar que los resultados devueltos solo incluyan documentos a los que el usuario solicitante tenga acceso.

#### Scenario: Usuario busca información restringida
- **WHEN** un usuario realiza una búsqueda que coincide semánticamente con un documento confidencial al que no tiene acceso
- **THEN** el motor de búsqueda omite dicho documento de los resultados devueltos
