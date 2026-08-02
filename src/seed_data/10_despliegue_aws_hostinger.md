# Evaluación de Arquitectura de Despliegue: CTI Soluciones (AWS vs Híbrido / Local)

> [!NOTE]
> Esta infraestructura no se aprovisionará de forma inmediata. Se evaluará formalmente en la **Fase 3** mediante un Registro de Decisión Arquitectónica (ADR) con base en los hallazgos de volumen de datos, tráfico y presupuesto recopilados en las Fases 1 y 2.

## 1. Dominio y DNS (Hostinger)
- **Dominio Corporativo:** CTI Soluciones (adquirido en Hostinger).
- **Configuración DNS:** Apuntamiento flexible mediante registros DNS A/CNAME hacia el entorno seleccionado (AWS EC2 / ALB o VPS / Servidor dedicado).

## 2. Candidato A: Infraestructura Cloud en AWS (VPC + EC2)
- **Experiencia Previa:** Prototipo con VPC personalizada (`172.31.0.0/16`), subredes públicas, Internet Gateway y grupos de seguridad (puertos 80/443/SSH).
- **Cómputo:** EC2 (`t3.micro` o superior) con NGINX reverse proxy administrando contenedores Docker / Next.js.
- **Criterios de Evaluación en Fase 3:** Costo recurrente mensual (OPEX), latencia, facilidad de escalado y respaldos S3.

## 3. Candidato B: Servidor Local / Híbrido (Hyper-V + NAS)
- **Entorno:** Hyper-V en Windows Server con almacenamiento NAS (Synology/QNAP) y conectividad segura.
- **Criterios de Evaluación en Fase 3:** Costo inicial (CAPEX), control total del hardware e integración directa con Active Directory on-premises.

## 4. Identidad Visual Base (CTI Soluciones)
- **Paleta de Colores:** Modo oscuro (fondos `#15181D` / `#1D2026`) y azul primario `#0270D7`.
- **Tipografía:** `IBM Plex Sans` para imagen de ingeniería técnica.

## 5. Estrategia de Producto Estrella
- **Sitio Web Público:** Portal corporativo CTI Soluciones.
- **Producto Estrella:** **Intranet Empresarial a la Medida con Búsqueda Profunda (Deep Search con IA / RAG)**.
