---
name: ky-design-to-html
description: Convert visible UI references such as screenshots, exported mockups, Figma frame images, SaaS empty states, dashboards, and landing page screenshots into high-quality HTML/CSS by decomposing layout, separating visual assets from code-rendered UI, implementing the page, then validating with browser screenshots and iterative visual correction. Use when the user asks to recreate, copy, convert, or implement a visual design as HTML/CSS from an image or equivalent visual reference. Do not use for ordinary frontend feature work without a visual reference, designing new pages from text only, backend work, or pure image generation.
---

# KY Design to HTML

## Core Rule

Do not jump directly from image to HTML.

Treat design recreation as an error-reduction loop:

1. Read the visual reference and produce a page map.
2. Split elements into code-rendered UI and external visual assets.
3. Decide the reference canvas, display viewport, and scaling strategy.
4. Build the HTML/CSS structure with fixed asset slots.
5. Render in a real browser and capture screenshots.
6. Compare the screenshot with the reference.
7. Correct specific visual errors and repeat when needed.

The skill exists to avoid cheap-looking output caused by asking the model to solve layout, style, and complex asset creation in one step.

Keep analysis compact. Produce enough page-map detail to guide implementation, but do not spend large token budgets describing obvious UI unless the user asks for a detailed teardown.

## Inputs To Establish

Before implementation, infer or ask only when necessary:

- Visual reference: screenshot, mockup image, Figma export image, browser screenshot, or another concrete visual artifact.
- Reference canvas: use the image dimensions and aspect ratio when available; otherwise choose a reasonable desktop canvas and note it.
- Display viewport: the browser/window size used to preview the result.
- Output type: single HTML file, project component, or app route.
- Asset availability: original logos, illustrations, product images, icons, screenshots, or only the reference image.
- Responsive scope: desktop only unless the user asks for mobile or the existing app requires it.

Do not trigger this workflow for a page idea described only in prose. In that case, use normal frontend/product design judgment instead.

## Permission Posture

Default to low permission and local-only work:

- Read the user's visual reference and existing project files.
- Write HTML/CSS/assets inside the project or requested output directory.
- Use host-native browser/screenshot tooling when available.
- Do not install dependencies, download packages, call image generation, or write global skill directories unless the user explicitly asks or approves.
- If screenshot verification requires unavailable tooling, state the limitation instead of silently skipping validation or expanding permissions.

## Step 1: Page Map

Start by creating a brief page map before writing code. Capture:

- Overall layout: columns, rows, primary regions, approximate ratios.
- Component inventory: top-to-bottom and left-to-right list of visible UI pieces.
- Color system: background, surfaces, borders, text, accents, approximate HEX values.
- Typography: title/body/helper sizes, weights, line-height feel, casing.
- Spacing and shape: density, padding rhythm, border radius, shadow softness.
- Complex visual assets: logo, illustration, product screenshot, 3D visual, people photo, brand hero, empty-state image.

This map becomes the implementation checklist. Keep it concise unless the user is explicitly asking for analysis.

## Step 2: Asset Separation

Classify each visual element before coding.

Render with HTML/CSS:

- Layout regions, navigation, sidebars, panels, cards, forms, tables, buttons, labels, badges, dividers, text, simple charts, simple icons from an existing icon library.

Treat as assets:

- Logos, complex illustrations, product screenshots, 3D objects, brand key visuals, people photos, detailed empty-state art, complex decorative artwork.

Use this test: if removing the element leaves the page structure intact, it is probably an asset. If removing it breaks the UI skeleton, it is probably code-rendered structure.

Do not hard-draw logos or complex illustrations with CSS or ad hoc SVG. Use existing assets when available. If only the reference image exists, crop or preserve the visual as a separate image when practical. Image generation or image editing is optional and should only be used when the user explicitly requests redrawing, upscaling, or transparent-background asset creation.

For detailed asset decisions, read `references/asset-handling.md`.

## Step 3: Set Canvas Fit

Before detailed styling, decide how the recreated design should fit the browser.

For screenshot recreation, distinguish:

- Reference canvas: the artboard being copied, usually the source image width/height.
- Display viewport: the user's current browser window or screenshot viewport.

Do not let a fixed-size desktop mockup overflow, crop, float in a corner, or compress into the browser by accident.

If the output is a standalone HTML preview of a large design, prefer a responsive fixed-aspect-ratio stage. Build inside the stage with percentages, grid tracks, and container-relative sizing when practical:

```css
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
}

.preview-shell {
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #000;
}

.design-stage {
  width: min(100vw, calc(100vh * 2048 / 1243));
  max-height: 100vh;
  aspect-ratio: 2048 / 1243;
  position: relative;
  overflow: hidden;
}
```

Use this pattern when the page is primarily a visual reproduction and does not need a production responsive layout.

If the implementation already uses a fixed-pixel artboard, never apply `transform: scale(...)` directly to the centered canvas without also sizing its layout box. CSS transforms change the visual size but not the layout size, which causes large black margins, off-center previews, and clipped right/bottom edges.

Use a three-layer pattern instead:

```css
html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
}

:root {
  --scale: 1;
}

.preview-shell {
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #000;
}

.scale-frame {
  position: relative;
}

.design-canvas {
  width: 2048px;
  height: 1243px;
  transform: scale(var(--scale));
  transform-origin: top left;
}
```

```html
<div class="preview-shell">
  <div class="scale-frame">
    <main class="design-canvas">...</main>
  </div>
</div>
<script>
  const designWidth = 2048;
  const designHeight = 1243;
  const frame = document.querySelector(".scale-frame");

  function fitCanvas() {
    const scale = Math.min(1, innerWidth / designWidth, innerHeight / designHeight);
    frame.style.width = `${designWidth * scale}px`;
    frame.style.height = `${designHeight * scale}px`;
    document.documentElement.style.setProperty("--scale", scale);
  }

  addEventListener("resize", fitCanvas);
  fitCanvas();
</script>
```

In the fixed-pixel pattern, `.scale-frame` provides the scaled layout size; `.design-canvas` provides the unscaled reference coordinate system. This keeps the preview centered and fully visible.

The fixed-pixel example caps scale at `1` to avoid blurry upscaling. Remove that cap only when the user wants the preview to fill a larger display.

Use these stage patterns for visual previews and pixel-oriented recreation. For real responsive app screens, implement responsive layout normally, but still preserve the reference aspect ratio at the target breakpoint before adding other breakpoints.

## Step 4: Build The HTML/CSS

Implement the first pass as structure-first:

- Match page proportions and alignment before polishing details.
- Match the reference canvas dimensions or aspect ratio before tuning individual components.
- Create stable dimensions for repeated UI units, toolbars, cards, and asset slots so images do not resize the layout.
- Use `object-fit`, explicit width/height, max constraints, and transparent placeholders for asset slots.
- Prefer the repo's existing framework, component patterns, styles, and icon libraries.
- If building a standalone artifact, choose simple semantic HTML/CSS or a minimal app structure appropriate to the user's request.

Asset placeholders are acceptable in the first pass if real assets are not available. Label them in code only when useful; do not add visible explanatory text to the UI unless the design shows it.

## Step 5: Render And Screenshot

After implementation, render the result in a real browser. Use the reference canvas dimensions for fidelity screenshots when possible. Also test the intended display viewport when the user will open the HTML in a different-sized browser.

Options:

- Use the available browser tool for local web targets.
- Use project-native test or screenshot tooling when present.
- Use `scripts/screenshot_page.py` for simple static pages if Python Playwright is available.

Always inspect the rendered screenshot. Code review alone is insufficient for visual recreation.

Before comparing details, verify canvas fit:

- The whole reference canvas is visible unless intentional scrolling is part of the target.
- The preview is centered in the display viewport.
- There is no unexpected large empty band around the design.
- The right and bottom edges are not clipped.
- UI elements are not compressed differently on the x and y axes.

If screenshot verification cannot run because of missing tools, sandbox limits, or dependency issues, clearly tell the user what was not verified and why. Do not install Playwright or browsers just to satisfy this step unless the user approves.

## Step 6: Compare And Correct

Compare the browser screenshot to the reference by region. Convert "doesn't look right" into concrete corrections:

- Canvas fit, aspect ratio, scaling, crop, overflow, or unwanted compression.
- Element position, width, height, alignment, margin, or padding.
- Font size, weight, line height, color, wrapping, or hierarchy.
- Surface, border, shadow, radius, opacity, or background mismatch.
- Asset size, crop, resolution, aspect ratio, or style mismatch.
- Overall density: too loose, too cramped, too heavy, too empty.
- Responsive breakage when mobile/tablet scope is required.

Read `references/visual-error-taxonomy.md` when the page looks close but still feels cheap or off.

Iterate: edit, render, screenshot, compare again. Stop when remaining differences are either minor, blocked by missing assets, or outside the requested scope.

## Delivery

When finishing, report:

- What was implemented.
- Which assets were used, missing, cropped, or represented by placeholders.
- What viewport(s) were verified.
- Any remaining visual gaps or unverified assumptions.

Do not imply pixel-perfect fidelity unless screenshot comparison supports it.
