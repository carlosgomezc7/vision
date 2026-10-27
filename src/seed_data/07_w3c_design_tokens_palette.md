# W3C DTCG Design Tokens and Theming

Design tokens form the single source of truth for the client's visual brand. VISION adheres strictly to the W3C Design Tokens Community Group (DTCG) specification:

```json
{
  "color": {
    "primary": {
      "$value": "#2563EB",
      "$type": "color",
      "$description": "Primary brand color for buttons and highlights"
    }
  }
}
```

Tokens are converted into CSS Custom Properties (`:root { --color-primary: #2563EB; }`) or Tailwind extensions via the `export_tokens_to_stylesheet` tool.
