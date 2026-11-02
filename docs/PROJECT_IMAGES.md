# Maintain project-card images

Use an actual reviewed project screenshot, render, plot, or photograph. Record
its public origin in `projects.json` and describe what the image really shows.
For website screenshots, prefer a repeatable capture script in the source
project's repository so future homepage changes can refresh the same asset.

## Recipes: capture in the source repository

Follow the Recipes repository's
[homepage screenshot checklist](https://github.com/rharriszzz/recipes/blob/main/docs/project-card-screenshot.md).
Its `npm run capture:homepage-card` command rebuilds the current checkout and
captures the heading, introduction, and complete recipe list without the empty
right side. Review and push `images/homepage-card.png` there first.

The maintained catalog metadata is:

```json
"image": {
  "url": "https://raw.githubusercontent.com/rharriszzz/recipes/main/images/homepage-card.png",
  "alt": "Actual Recipes homepage screenshot showing the Recipes heading, introduction, and single-column list of recipe links on ivory paper.",
  "caption": "Actual Recipes homepage screenshot · complete recipe list",
  "source": "https://github.com/rharriszzz/recipes/blob/main/images/homepage-card.png"
}
```

Keep this stable URL when refreshing the screenshot. If the filename and meaning
stay the same, no index commit or redeployment is needed; the card loads the
updated hosted PNG directly, subject to browser/CDN caching. Do not copy the
image into `assets/images/` as well.

## FFT Image Explorer: regenerate the computed illustration

The [approved two-panel figure](https://github.com/rharriszzz/fft-image-explorer/blob/main/docs/figures/local-fft-card.png)
is generated from the original bead photograph, saved centerline, Gaussian
spatial window, and calculated FFT. It is **not** a screenshot of the app.
The source repository owns `docs/figures/local-fft-card.png`.

Follow its [reproducibility documentation](https://github.com/rharriszzz/fft-image-explorer/blob/main/docs/fft-figures.md)
and run `python3 scripts/generate_fft_figures.py` in that repository.
Review both the full 1600 × 1000 illustration and its 400 × 250
`local-fft-card-preview.png` before publishing changes. The index uses the
stable main-branch raw PNG and never copies or regenerates it.

## Bead Map: regenerate the approved mask illustration

The approved [two-panel image](https://github.com/rharriszzz/bead_map/blob/main/docs/figures/bead-map-card.png)
shows the original necklace photograph next to the color-coded selections from
the repository's three committed mask images, with identical source coordinates.
It is a mask illustration, not a screenshot or a validated reconstruction.

The Bead Map repository maintains `docs/figures/bead-map-card.png`. To regenerate:

```sh
python3 -m pip install 'Pillow==12.1.1'
python3 scripts/generate_bead_map_figures.py
```

Review both that 1200 × 660 image and its
`docs/figures/bead-map-card-400.png` preview. Keep the mask color
assignments and crop correspondence truthful. Commit and push the source PNG
there before relying on it in the index. The index embeds the stable hosted
image without making an additional copy.

## HSV Tools: regenerate the reviewed picker illustration

The [reviewed red-bead HSV selection figure](https://github.com/rharriszzz/hsv_tools/blob/main/docs/figures/hsv-tools-card.png)
pairs the real necklace photograph and its actual HSV Picker line-selection
mask. It is a computed composite, not a literal screenshot of the OpenCV
window and not a finished bead-color reconstruction.

The HSV Tools repository maintains `docs/figures/hsv-tools-card.png` and
its `docs/figures/hsv-tools-card-preview.png`. To regenerate, install
`requirements-figures.txt` in a suitable environment, then run:

```sh
python scripts/generate_hsv_figures.py
python -m unittest discover -s tests -v
```

See the [full figure notes](https://github.com/rharriszzz/hsv_tools/blob/main/docs/figures.md)
for exact sampled coordinates, HSV tolerances and scientific provenance.
Review the 1600 × 1000 original and the 400 × 250 preview before
publishing. The directory embeds the stable hosted PNG from the
source repository without copying it.

## Validate and publish an index change

If image metadata changes, update `projects.json`, the provenance notes in
[`INVENTORY.md`](INVENTORY.md), and the relevant regression test if the reviewed
source path changes. Record checks actually performed in
[`VALIDATION.md`](VALIDATION.md); distinguish local preview checks from live
verification. A focused image refresh does not require changing the catalog's
full-inventory `verifiedOn` date.

Run from the index repository root, after the source image is public:

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/check_links.py
git diff --check
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Inspect http://127.0.0.1:8000/ at desktop and mobile widths. Confirm that the
updated project image loads, key content remains visible, and its caption and alt
text are accurate. Stop the preview with Ctrl-C. Unit tests check metadata and
rendered HTML; the link checker checks reachability. Neither replaces opening
the card in a browser.

Stage only intended changes, review them, commit, and push to `main`. Generated
`dist/` stays uncommitted. Wait for the
[index Actions workflow](https://github.com/rharriszzz/rharriszzz.github.io/actions)
to finish successfully, then run:

```sh
python3 scripts/check_links.py --base-url https://rharriszzz.github.io/
```

Open [the live directory](https://rharriszzz.github.io/) and verify that the
updated card displays the intended PNG from its real public URL, without a
placeholder or local request override. If it looks stale, check the raw source PNG and
allow browser/CDN caches to refresh. Finish with a clean `git status` and a brief
record of commits, check results, and the live URL.

## Other project images

For hosted PNG/JPG/WebP images, the validator allows `image.url` only
under the owning project's `raw.githubusercontent.com` branch, in its
`images/` or `docs/figures/` directory. Use its GitHub file page for `image.source` and meaningful alt text
and a factual caption. Choose exactly one of `image.url` and `image.path`.

For local reviewed assets, use `image.path` under `assets/images/`; only
referenced images are copied into the build. Keep provenance and any capture
instructions with the source project, and link them here when introducing a new
repeatable capture workflow.
