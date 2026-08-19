# Process spine

A dark-theme layout template for any staged, gated process. Stages render as circles because they
are periods of work. Gates render as diamonds because they are decisions. A switch toggles between
a full gate set and a reduced one.

**This repository contains no organisational content.** Every stage name, gate name, question, and
output in `index.html` is a placeholder. Real process content belongs in your own system of record,
never in this file.

## Structure

```
index.html              complete markup; readable with JavaScript disabled
assets/css/tokens.css   palette and type tokens; swap for your own brand
assets/css/spine.css    component styles; references tokens only, no literals
assets/js/spine.js      gate-set switch and optional deep links
assets/fonts/           Archivo (SIL Open Font License), four weights, WOFF2
```

No build. No npm. Open `index.html` in a browser and it works.

## Behaviour

- Works with JavaScript disabled; the script only adds the switch and links.
- Honours `prefers-reduced-motion`.
- The rail scrolls inside its own container, so the page never scrolls sideways on mobile.
- Optional deep links: pass `?base=<encoded https://…sharepoint.com/… url>` and the nodes become
  links that open in the parent frame. Only a `*.sharepoint.com` origin is accepted.

## Fonts

Archivo is bundled under the SIL Open Font License. Regenerate the WOFF2 files with
`tools/convert-fonts.sh <path-to-ttf-directory>` if you need other weights.
