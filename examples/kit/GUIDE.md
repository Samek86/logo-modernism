# LogoModernism — Identity Guide (Effect C, v1)

## 1. Construction
- **Idea:** one square split by a single Z-shaped channel into two identical L-slabs, each the 180° rotation of the other. It reads as a solid block and as motion (a step or switch) at once.
- **Grid:** 256 viewBox, 8-unit module. Mark spans 32–224 (24 modules).
  - Channel = **2 modules (16)**, uniform everywhere.
  - Slab bar = **7 modules (56)** × full width.
  - Slab leg = **11 × 8 modules (88 × 64)**.
  - Silhouette is a closed square. Channel ends exit at the left and right edges only.
- **Files:**

  | File | Use |
  |---|---|
  | `mark.svg` | Master, `currentColor`. Use at 32px and up. |
  | `mark-16.svg` | Small-size cut on a 16px grid: 2px channel, 4px bars. Use at 24px and below. |
  | `mark-reversed.svg` | White mark on black rounded square (r = 56/256). Also the app-icon source. |
  | `favicon.svg` | Favicon source: master geometry on the tile. |
  | `favicon.png` | 32px favicon. |
  | `app-icon.png` | 512px app icon. |
  | `lockup-horizontal.svg` | Mark + wordmark, all paths. Primary lockup. |
  | `lockup-stacked.svg` | Mark + wordmark, all paths. |

- **Wordmark:** hand-built orthogonal sans, outlined paths (no font).
  - Cap 100, x-height 72, verticals 17, horizontals 14 (optical compensation), tracking 18.
  - Horizontal lockup: cap height = ½ mark height; gap = X.
  - Stacked lockup: cap height = 0.30 × mark height; gap = X, centred.

## 2. Clear space
- **X = slab bar height = 7/24 of the mark's height.**
- Keep X empty on all four sides of the mark and of each lockup. The lockup SVGs already include X in their viewBox.

## 3. Minimum size

| Asset | Minimum |
|---|---|
| Mark (`mark.svg`) | 32px / 8mm |
| Mark below 32px | Switch to `mark-16.svg` (crisp at 16, acceptable at 24) |
| Horizontal lockup | 160px / 40mm wide (mark ≈ 24px) |
| Stacked lockup | 120px / 30mm wide |

## 4. Colour

| Name | Hex | Role |
|---|---|---|
| Black | `#000000` | Primary mark colour |
| White | `#FFFFFF` | Reversed mark, grounds |
| International Orange | `#FF4F00` | Accent — fields, backgrounds, highlights only |

- The mark is always solid black or solid white.
- On orange, use a black mark.

## 5. Don'ts
- Don't set the mark in orange on white (weak contrast, dilutes the black/white identity).
- Don't change the channel width, round the corners, or reopen the square's corners.
- Don't rotate, mirror, skew, outline, add shadows, gradients or effects.
- Don't retype the wordmark in a font. Use the supplied paths only, and don't re-space them.
- Don't place the master below 32px. Use `mark-16.svg` instead.
- Don't crowd the clear space, or put the mark on busy photos without a solid field.
- Don't recolour the two slabs differently. It is one shape split, not two logos.
