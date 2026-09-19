# Technology Stack and Enterprise Architecture

Intranets developed by CTI Soluciones follow a robust and modern standard:

## Official Technology Stack
- **Frontend:** Next.js (App Router), Tailwind CSS, Shadcn UI for clean and accessible components.
- **Backend & Database:** Supabase (PostgreSQL) with native support for `pgvector`.
- **Authentication:** Supabase Auth with OAuth/SAML integration for Microsoft 365 / Google Workspace.
- **Deployment and CI/CD:** Vercel or dedicated servers with Docker containers.

## Code Patterns
- Strict modularity by business domains.
- Strict typing with TypeScript.
- Test coverage on critical authentication and permissions flows (RBAC).
