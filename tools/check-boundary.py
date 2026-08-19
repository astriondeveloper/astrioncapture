#!/usr/bin/env python3
"""Fail if anything that belongs behind SharePoint has leaked into the repo.

Scans what a visitor actually receives, so it deliberately ignores two places
where these phrases appear legitimately as declarations of what is excluded:
HTML comments (never rendered) and the README section that documents the
boundary. Everything else is fair game.

Run before every push:  python3 tools/check-boundary.py
"""
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

RULES = [
    ("value threshold / authority matrix",
     r"\$ ?50 ?m|50M TCV|President, (SPG|Mission Solutions)|decision authority is"),
    ("gate criteria and pass standards",
     r"pass standard|entrance criteri|non-waivable|what gate \d is not"),
    ("RASCI assignments",
     r"\bRASCI\b|owns the outcome and final accountability"),
    ("scoring model",
     r"opportunity quality score|scoring criterion|\bPwin\b|price[- ]to[- ]win"),
    ("named people",
     r"Weilbach|Huttenhoff|Doyle|Steiner|Safford|Elder|Neumuller|Hansborough|Armstrong"),
    ("named pursuits",
     r"\bMUSE\b|TSOMIS|RAPTER|Megatron|ROSIE"),
    ("tenant urls",
     r"[a-z0-9-]+\.sharepoint\.com/sites/"),
]

SKIP_DIRS = {".git", "assets/fonts", "assets/img"}
README_EXCLUDED_SECTION = "## What is deliberately not here"


def visible_text(path: pathlib.Path) -> str:
    text = path.read_text(errors="ignore")
    if path.suffix in {".html", ".htm"}:
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    if path.name == "README.md":
        # drop only the section that documents the boundary
        start = text.find(README_EXCLUDED_SECTION)
        if start != -1:
            end = text.find("\n## ", start + 1)
            text = text[:start] + (text[end:] if end != -1 else "")
    return text


def main() -> int:
    failed = False
    files = [
        p for p in ROOT.rglob("*")
        if p.is_file()
        and not any(s in str(p.relative_to(ROOT)) for s in SKIP_DIRS)
        and p.suffix in {".html", ".css", ".js", ".md", ".json", ".txt"}
    ]
    for label, pattern in RULES:
        hits = []
        rx = re.compile(pattern, re.I)
        for p in files:
            for n, line in enumerate(visible_text(p).splitlines(), 1):
                if rx.search(line):
                    hits.append(f"  {p.relative_to(ROOT)}:{n}: {line.strip()[:100]}")
        if hits:
            failed = True
            print(f"LEAK  {label}")
            print("\n".join(hits[:5]))
        else:
            print(f"clean {label}")
    print("\nBOUNDARY FAILED - do not push" if failed else "\nBoundary holds.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
