# SaaS Multi-Tenant Architecture — CTI Soluciones Intranet

## Architectural Decision (2026-08-02)
The project has evolved from a single-company Intranet to a **Multi-Tenant SaaS** model where multiple client companies register, get a 30-day trial, and configure their private portal.

## Data Model (Supabase/PostgreSQL)
Tables created with Row Level Security (RLS):
- **organizations**: Registered companies (name, logo_url, trial_start_date, is_active).
- **profiles**: Users linked to an organization with a role (admin/employee). Extends auth.users.
- **announcements**: Corporate announcements per organization.
- **documents**: Downloadable files/formats per organization (Supabase Storage).
- **time_off_requests**: Vacation requests with statuses (pending/approved/rejected).

## Data Isolation (RLS)
The `get_user_org_id()` function was created to retrieve the `organization_id` of the authenticated user. All RLS policies filter by this function, ensuring Company A never sees Company B's data.

## Onboarding Flow
1. User registers at `/login` → Supabase creates auth.user → Trigger `handle_new_user` creates a row in `profiles` with role 'admin'.
2. The `actions.ts` code automatically creates an `organization` and links it to the new user's profile.
3. The user is redirected to `/dashboard` where they can configure their company.

## Product Types (Service Selector)
Each organization can choose from 3 modalities:
1. **Presentation Page**: Public services landing page only.
2. **Intranet**: Private corporate portal with internal modules (announcements, time-off, documents).
3. **Hybrid**: Combination of both — public landing + private intranet.
