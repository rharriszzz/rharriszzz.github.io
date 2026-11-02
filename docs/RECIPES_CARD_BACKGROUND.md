# Recipes card: continue the screenshot's background to the card edges

## What the user wants

On the [central project index](https://rharriszzz.github.io/), keep the
**authentic, cropped Recipes homepage screenshot** as the Recipes card image.
Keep the typography, recipe names, exact crop, and source-image pixels. The
screenshot is a narrow portrait of the actual list. When shown in a wider
project-card image box, the otherwise empty area **must look like continuous
ivory paper**, not a second white rectangle or a redesigned screenshot.

This is not a request to extend the original website's layout or to invent
additional recipe links. Do not use generative image reconstruction or replace
the screenshot with a mockup.

## Source and cause

- Maintained screenshot: `rharriszzz/recipes/images/homepage-card.png`.
  The central index embeds its existing
  `https://raw.githubusercontent.com/rharriszzz/recipes/main/images/homepage-card.png`
  URL, and does **not** store a duplicate.
- Screenshot generation is documented in
  [Recipes' capture instructions](https://github.com/rharriszzz/recipes/blob/main/docs/project-card-screenshot.md)
  and implemented by `scripts/capture_homepage_card.mjs` in that repository.
  The capture includes the real page's heading, introduction, and complete list,
  cropped to the content with a small inset. The reviewed PNG was 1056 × 1300
  pixels when this adjustment was made.
- The Recipes homepage's paper color is `#fffff0`, set by
  `--paper: #fffff0` in `rharriszzz/recipes/static/style.css`.
- The central index displays project images in a comparatively wide 16:10
  image box using `object-fit: contain`. Before the fix, the general
  `.project-image` rule gave the extra space a **white `#fff`** background,
  and the surrounding `figure` used a pale green background. The mismatch
  made the real screenshot look as if it stopped short of the card edges.

## Implemented fix

In this index repository's `style.css`, a selector scoped specifically to
`data-project="recipes"` sets both its image and figure background to the
same `#fffff0` as the Recipes page:

```css
.project-card[data-project="recipes"] figure,
.project-card[data-project="recipes"] .project-image {
  background: #fffff0;
}
```

This keeps the original screenshot and crop unchanged. It fills only the
unused letterbox area with the exact paper color, so it looks as though the
background continues to the edges of the card. The CSS is intentionally
**Recipes-specific**; other project cards retain their own appearance.

## How to revise or verify later

1. If the Recipes homepage changes, refresh its real screenshot using
   `npm run capture:homepage-card` in the **Recipes** repository; review the
   actual PNG. The central index loads it by its existing URL.
2. If Recipes' paper background changes, inspect
   `recipes/static/style.css` (and sample a clear, text-free area of the
   PNG if needed). Update this index's Recipes-specific color accordingly.
3. Check the entire screenshot and its surrounding image box at desktop
   and mobile widths. The list must remain intact, without stretching,
   distortion, invented text, clipping, or visible color seams. Keep the
   existing caption and destination link.
4. Run `python3 -m unittest discover -s tests -v` in the central index
   repository, and check its
   [GitHub Actions deployment](https://github.com/rharriszzz/rharriszzz.github.io/actions)
   before verifying the [live page](https://rharriszzz.github.io/).
   If a live change seems missing, check browser/CDN caching.

If a future requirement truly calls for a **modified PNG rather than visual
CSS continuation**, derive it from the existing authentic PNG with a
deterministic image operation: sample its paper color and paste the original,
unaltered pixels on a larger `#fffff0` canvas. Do not re-render, retype,
or generatively imitate the recipe list. Any such asset would require a
corresponding update to its capture/maintenance workflow and provenance notes.
