# NKAI DataShare Website

Astro + Starlight website for the NKAI DataShare resource repository.

## Commands

| Command | Purpose |
| --- | --- |
| `npm install` | Install locked dependencies |
| `npm run dev` | Start the local development server |
| `npm run check` | Run Astro and TypeScript checks |
| `npm run build` | Check and create the production build |
| `npm run index` | Regenerate resource metadata from the repository root |
| `npm run validate:index` | Validate resource metadata and encoded links |

The production build contains only site assets and JSON metadata. Course resource files remain in the repository and are opened using GitHub or Raw URLs.
