#!/usr/bin/env bash
# One-time conversion of the company-issued Archivo TTFs to WOFF2.
# The output is committed, so this does not run as part of any build.
# Re-run only if the brand standard reissues the font files.
set -euo pipefail

SRC="${1:-/root/.claude/skills/synced/astrion-brand/assets/fonts}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/assets/fonts"

python3 -c "import fontTools" 2>/dev/null || pip install fonttools brotli

python3 - "$SRC" "$DEST" <<'PY'
import sys, os
from fontTools.ttLib import TTFont
src, dest = sys.argv[1], sys.argv[2]
for weight in ("Regular", "Medium", "SemiBold", "Bold"):
    f = TTFont(os.path.join(src, f"Archivo-{weight}.ttf"))
    f.flavor = "woff2"
    out = os.path.join(dest, f"Archivo-{weight}.woff2")
    f.save(out)
    print(f"{out}  {os.path.getsize(out)//1024} KB")
PY
