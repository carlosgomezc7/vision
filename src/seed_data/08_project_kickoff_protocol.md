# Project Kickoff and Client Readiness Protocol

When starting a new landing page project with VISION:

1. Step 1 — Client Intake & Listening:
   Listen to the client and fill `client_discovery_template.json` or gather notes.
2. Step 2 — Readiness Audit:
   Execute `audit_client_readiness_score(payload)`. If the score is < 80%, send the generated follow-up questions to the client.
3. Step 3 — Token Generation & Accessibility Audit:
   Execute `generate_design_tokens_w3c` and `audit_theme_palette`.
4. Step 4 — Formal Specification:
   Execute `create_landing_page_specification` with company name, sections, CTA goal, and visual style.
5. Step 5 — Code Scaffolding:
   Generate modular components in `src/components/landing/*` and verify the production build.
