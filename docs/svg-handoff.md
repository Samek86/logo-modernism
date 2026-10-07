# SVG handoff rules (merged)

Synthesized from svg-gen + logo-design craft + this skill’s modernist defaults.

1. **Root**: `xmlns`, deliberate `viewBox` (symbols `0 0 256 256` or `0 0 100 100`). Prefer no fixed width/height for app use.
2. **Groups**: `<g id="symbol">`, `<g id="wordmark">`; prefix IDs if multiple SVGs on one page.
3. **Color**: exploration = black; masters often `currentColor` for mono; brand colour only after checkpoint.
4. **A11y**: `role="img"` + `<title>` (and `<desc>` when needed); decorative icons `aria-hidden="true"`.
5. **Chat**: attach **PNG** preview; keep SVG as source of truth.
6. **Optimize**: few anchors, trim decimals, no editor junk, no live `<text>` in finals.
7. **Variants after approval**: black / white / mono / square / favicon (`scripts/export_variants.py`).
