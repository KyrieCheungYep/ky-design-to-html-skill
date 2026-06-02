# Visual Error Taxonomy

Use this reference after browser screenshot verification when the result is functional but does not yet match the reference or feels lower quality.

## Compare By Region

Move through the page in a stable order:

1. Overall canvas and viewport.
2. Header or top navigation.
3. Sidebar or primary navigation.
4. Main content regions.
5. Cards, tables, forms, or repeated components.
6. Primary assets.
7. Footer or lower regions.

For each region, state the difference as an actionable edit.

Bad: "The hero is off."

Good: "The hero image is about 15% too tall, the headline starts 32px too low, and the CTA gap should be closer to 12px than 24px."

## Error Categories

### Canvas Fit

Symptoms:

- The generated preview looks good, but the opened HTML is squeezed, cropped, or packed into one corner.
- The design is visually correct but appears small with a large empty band above or around it.
- The right sidebar or bottom player is cut off even though the design was meant to fit one screen.
- The design was recreated at one artboard size but displayed in a different browser aspect ratio.
- Fixed pixel widths overflow the viewport.
- The page fills `100vw` and `100vh` even though the reference has a different aspect ratio.
- A transformed canvas is centered by its unscaled layout box instead of its scaled visual box.

Fixes:

- Separate the reference canvas from the display viewport.
- Use a fixed-aspect-ratio stage for standalone visual previews.
- Scale fixed-pixel artboards with a three-layer wrapper: shell, scaled layout frame, unscaled design canvas.
- Do not apply `transform: scale(...)` directly to a centered fixed-size canvas unless a parent frame also reserves the scaled width and height.
- Verify both the reference-size screenshot and the intended user-facing viewport.

### Layout

Symptoms:

- Columns have wrong proportions.
- Content starts too high, low, left, or right.
- Cards do not align to the same grid.
- Elements wrap when the reference keeps them on one line.

Fixes:

- Adjust grid/flex ratios, container width, padding, margins, gap, alignment, and min/max widths.
- Use stable dimensions for fixed-format UI.

### Typography

Symptoms:

- Page feels heavy, dull, sparse, or template-like.
- Text wraps at the wrong point.
- Headings overpower or underplay the reference.

Fixes:

- Tune `font-size`, `font-weight`, `line-height`, `letter-spacing`, max width, and text color.
- Prefer the existing project font. If unavailable, choose a close system fallback and report the gap.

### Color And Surface

Symptoms:

- Background hue is close but wrong.
- Borders are too visible or invisible.
- Shadows look dirty, harsh, or generic.
- Buttons lack the same contrast.

Fixes:

- Sample colors from the reference when possible.
- Tune border alpha, shadow blur/spread/opacity, surface contrast, and accent saturation.

### Asset

Symptoms:

- Logo is distorted or fake.
- Illustration is blurry, low-detail, or a different style.
- Screenshot crop is soft.
- Asset is too large, too small, or misaligned.

Fixes:

- Preserve aspect ratio.
- Use a better source asset or crop.
- Adjust asset slot dimensions, `object-fit`, and alignment.
- Report missing or low-quality assets rather than hiding the issue.

### Density

Symptoms:

- The page feels too loose, too cramped, too empty, too loud, or too compressed even when individual values seem plausible.

Fixes:

- Adjust spacing systems in groups instead of tweaking isolated pixels.
- Compare vertical rhythm, card padding, menu item height, and section gaps.

### Responsive

Symptoms:

- Desktop matches but mobile breaks.
- Fixed widths overflow.
- Text collides with controls.
- Assets dominate small screens.

Fixes:

- Add breakpoints for major layout changes.
- Reduce asset scale, stack columns, constrain text, and preserve tap targets.

## Cheapness Checklist

If the screenshot is technically close but still feels AI-generated, inspect:

- Font weight too bold or too uniform.
- Line height too loose.
- Border radius repeated everywhere without hierarchy.
- Shadows too dark or too large.
- Spacing lacks a consistent rhythm.
- Asset quality is below the surrounding UI.
- Icon style is inconsistent.
- Palette is dominated by one hue family without enough neutral structure.

## Final Judgment

Do not chase every pixel by default. Prioritize differences visible at normal viewing size:

- Structure first.
- Typography and density second.
- Colors and surfaces third.
- Asset quality whenever it affects perceived professionalism.
