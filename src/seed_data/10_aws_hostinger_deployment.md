# Deployment Architecture Evaluation: CTI Soluciones (AWS vs Hybrid / Local)

> [!NOTE]
> This infrastructure will not be provisioned immediately. It will be formally evaluated in **Phase 3** through an Architectural Decision Record (ADR) based on the data volume, traffic, and budget findings gathered in Phases 1 and 2.

## 1. Domain and DNS (Hostinger)
- **Corporate Domain:** CTI Soluciones (acquired at Hostinger).
- **DNS Configuration:** Flexible routing via DNS A/CNAME records pointing to the selected environment (AWS EC2 / ALB or VPS / Dedicated server).

## 2. Candidate A: Cloud Infrastructure on AWS (VPC + EC2)
- **Prior Experience:** Prototype with custom VPC (`172.31.0.0/16`), public subnets, Internet Gateway, and security groups (ports 80/443/SSH).
- **Compute:** EC2 (`t3.micro` or higher) with NGINX reverse proxy managing Docker / Next.js containers.
- **Phase 3 Evaluation Criteria:** Monthly recurring cost (OPEX), latency, scalability, and S3 backups.

## 3. Candidate B: Local / Hybrid Server (Hyper-V + NAS)
- **Environment:** Hyper-V on Windows Server with NAS storage (Synology/QNAP) and secure connectivity.
- **Phase 3 Evaluation Criteria:** Initial cost (CAPEX), full hardware control, and direct integration with on-premises Active Directory.

## 4. CTI Soluciones Base Visual Identity
- **Color Palette:** Dark mode (backgrounds `#15181D` / `#1D2026`) and primary blue `#0270D7`.
- **Typography:** `IBM Plex Sans` for a technical engineering image.

## 5. Star Product Strategy
- **Public Website:** CTI Soluciones corporate portal.
- **Star Product:** **Custom Enterprise Intranet with Deep Search (AI / RAG)**.
