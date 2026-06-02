# Asset Handling

Use this reference when a design contains logos, illustrations, product screenshots, hero images, empty-state art, 3D visuals, or other non-UI artwork.

## Default Position

Do not turn complex assets into CSS drawings or improvised SVGs.

The goal is not to generate assets by default. The goal is to prevent visual assets from damaging the HTML/CSS recreation.

Keep this workflow low-permission by default. Do not download images, install image-processing tools, call image generation, or write outside the project unless the user explicitly asks or approves.

## Classification

Code-rendered UI:

- Navigation, sidebars, tabs, menus, cards, panels, buttons, inputs, tables, badges, tags, dividers.
- Simple geometric icons when an existing icon library is available.
- Simple charts or progress indicators when fidelity does not depend on detailed artwork.

External assets:

- Brand logos and marks.
- Detailed empty-state illustrations.
- Product screenshots and app mockups.
- 3D objects or rendered devices.
- People, photos, textures, detailed hero art.
- Any element whose exact shape carries brand or composition quality.

Quick test: remove the element. If the page still reads as the same interface, treat the element as an asset.

## Preferred Asset Paths

1. Use the user's original asset files when available.
2. Crop from the supplied reference when the asset is only embedded in the screenshot and the crop quality is acceptable.
3. Use a neutral placeholder when the asset is missing and the user did not ask for asset generation.
4. Only use image generation or editing when explicitly requested.

If the available reference image is too low-resolution for a clean crop, preserve the layout slot and report the asset quality gap instead of pretending the final result is production-ready.

## Placement Rules

- Preserve aspect ratio unless the reference clearly distorts the asset.
- Set explicit slot dimensions or responsive constraints.
- Use `object-fit: contain` for logos and illustrations that must not crop.
- Use `object-fit: cover` only for photos or screenshots where cropping is acceptable.
- Prevent assets from determining layout dimensions unless the design intentionally does that.
- Use transparent PNG/WebP/SVG assets when layering over colored UI surfaces.

## Placeholder Rules

Placeholders should protect layout fidelity without pretending to be final assets.

- Match the approximate dimensions and location of the real asset.
- Use quiet neutral color or low-contrast outline.
- Do not add visible "asset missing" explanatory text unless this is outside the final UI surface.
- Report placeholders in the final response.

## Optional Transparent Background Work

Transparent asset creation is optional. Use it only when the user requests it or the available asset has an unwanted solid background.

If a green-screen asset is supplied, a simple chroma-key script can remove green pixels, but thresholds and edge feathering may need manual tuning. Avoid this path for pale green artwork or images with green content.

If no local image-processing library is available, do not install one by default. Use CSS placement with the best available asset and disclose the limitation.

## Common Failures

- CSS-drawn logo resembles the brand but feels fake.
- SVG illustration has the right colors but wrong detail density.
- Cropped screenshot asset is too low-resolution after scaling.
- Asset aspect ratio is stretched to fit the slot.
- Image dimensions push cards, heroes, or empty-state containers out of alignment.
- Generated assets introduce a different visual language than the UI.
