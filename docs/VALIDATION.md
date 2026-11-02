# Validation record

Reviewed on 2026-11-01.

## Local checks

- `python3 -m unittest discover -s tests -v`: **7 tests passed**. Covers the
  reviewed project inventory in static HTML, unsafe/private/duplicate-entry
  rejection, escaped content, image and anchor paths, accessibility markup, and
  the exact publication allowlist, including a stray-file exclusion test.
- `node --check app.js`: passed.
- `git diff --check`: passed.
- `python3 scripts/check_links.py`: **27 external URLs passed**, including all
  repository links, the two public Live Site links, and image source locations.
- Local HTTP preview returned 200. Generated output contains **13 files** and
  occupies about **3.3 MB**, with seven authentic project images and no runtime
  dependencies or external requests needed to render the directory.

## Browser review

Used the installed Chrome browser through native UI controls, with the local
HTTP server serving the actual generated `dist/` artifact.

- Desktop review: light theme, typography, navigation, introduction, and filters.
- Responsive review: 320 CSS-pixel narrow mobile viewport and 768 CSS-pixel
  tablet viewport. Single-column mobile cards, two-column tablet cards, wrapping
  filter controls, readable descriptions, and image panels were inspected.
- Corrected a fixed image-height issue discovered at 320 pixels, then reloaded
  and visually verified full screenshot proportions at mobile and tablet sizes.
- Inspected the generated Symphonium SVG and the neutral FFT panel in context.
- Browser-app category returns Reversi and Madweave, with Madweave explicitly
  labeled as source available and lacking a verified live link.
- Research plus `vortex` returns one project. An unmatched term returns the empty
  state. Reset restores all 16 projects, clears the URL query, and focuses search.
- Keyboard navigation (Option-Tab on this Mac’s Chrome configuration) reaches
  category controls; Space activates the Browser apps filter.
- With JavaScript disabled through DevTools, all 16 entries and repository/live
  links remain present, filter controls stay hidden, and the fallback explanation
  is shown. JavaScript was re-enabled after this check.
- The page console had no application messages on inspection.
- Reversi was exercised on its production URL: Black D3 triggered White C5, and
  the WebAssembly coach showed ranked continuations. Its screenshot captures
  this actual state.
- arXiv Shelf’s production introduction renders, describes both editions, and
  shows its public screenshot and source links. The permission-dependent hosted
  library is not offered as an unrestricted live app by this index.

These are Chrome desktop and responsive-emulation checks, not physical iPhone
or Safari certification. No screen-reader audit or automated accessibility score
is claimed; the implementation includes semantic landmarks, heading hierarchy,
native keyboard controls, alt text, live result status, skip navigation, visible
focus styling, reduced-motion support, and zoom-friendly viewport metadata.

## Publication boundary

Only the central repository is changed. The build copies explicitly named public
files, not the repository root or arbitrary asset directories. No private
repository data, PDFs, local libraries, user settings, credentials, investigation
snapshots, or files from other local checkouts enter the publication artifact.
The reference photograph is copied from the public Beads repository; the arXiv
screenshot is copied from its already public landing-page assets.

The deployment workflow runs the same tests and script syntax check, uploads only
`dist/`, and gives deployment permissions only to its main-branch deploy job.
Pull requests do not deploy.

## Production verification

- The initial [build and Pages deployment](https://github.com/rharriszzz/rharriszzz.github.io/actions/runs/41329443718)
  passed both jobs and published https://rharriszzz.github.io/.
- `python3 scripts/check_links.py --base-url https://rharriszzz.github.io/`:
  **39 URLs passed**, including every published image, stylesheet, script,
  favicon, catalog, project repository, public site, and image-source link.
- SHA-256 comparisons confirmed that the production HTML, catalog, CSS, JS,
  favicon, and all seven project images match the locally reviewed build exactly.
- The production page was opened in Chrome and showed the complete directory
  and active filter controls.
- Production requests for `README.md`, `scripts/build.py`, `docs/INVENTORY.md`,
  and `.git/config` returned **404**, as expected for the publication allowlist.
- The first run exposed deprecation warnings in older official Pages actions.
  The workflow was updated to the current official major releases: checkout,
  setup-python, and setup-node v7; configure-pages v6; upload-pages-artifact v5;
  deploy-pages v5. Versions were checked against their official GitHub releases.
  Subsequent runs are available in the repository’s Actions history.

## MadWeave follow-up — 2026-11-01

The featured MadWeave entry now links to its published GitHub Pages project site,
with a current description of patterns, palette colors, and static SVG artwork
export. Its note identifies the mouse/trackpad requirement and distinguishes
artwork download from future editable project saving. The original public
interface image remains the catalog image.

Before adding the live link, the MadWeave [test and deployment run](https://github.com/rharriszzz/madweave/actions/runs/41358872009)
passed. Chromium then opened the deployed landing page, guide, and editor at
1280, 390, and 320 CSS-pixel widths. There was no document-level horizontal
overflow, failed HTTP response, or JavaScript exception. On the public embedded
SVG, real pointer clicks changed a pattern, selected 24 strips per direction,
and changed spacing. Static SVG export downloaded successfully without scripts.
This is desktop Chromium responsive emulation, not physical touch-device testing.

The central index's seven Python tests, build, JavaScript syntax check, and
whitespace check pass with the changed catalog entry. The update is scoped to
MadWeave; it does not repeat the full repository inventory review.


## Editable MadWeave projects — 2026-11-01

The catalog now describes Save Project/Open Project and offline editing instead
of listing editable saving as future work. Self-contained HTML projects preserve
all design settings and include their engine, scripts, styles, and pattern
images. Original editable SVG import and static artwork export remain distinct.

The local project suite passes in Chromium and Firefox. Separate checks of the
installed Windows Chrome 156.0.8078.48, Edge 156.0.4314.58, and Firefox 158.0.1
passed offline opening, editing, saving, direct reopening, and Open Project in
isolated test profiles. The central catalog's seven tests and script syntax
check pass after its text update. Actual Mac browser checks remain with the
user; the project includes a short acceptance checklist.

The [three-engine test and deployment run](https://github.com/rharriszzz/madweave/actions/runs/41361706822)
passed Chromium, Firefox, WebKit, and deployment. On the public site, Chromium
then verified Save Project, direct offline opening, further editing and saving,
reopening that new copy, and Open Project importing it back into the site. The
landing page, guide, and editor fit three viewport widths, and static export
still worked. There were no page exceptions or failed HTTP responses.


## Simplified single-list layout — 2026-11-01

The index now renders every listed project in a single ordered card grid, with
Reversi first and HIS Profile last. The separate Selected / More groups, search,
category filters, no-results state, and client-side JavaScript were removed.
The page remains server-rendered static HTML; unlisted historical projects remain
excluded. The test suite now checks the single grid and absence of the removed UI.
The original browser-review notes above are a historical record of the earlier
layout, not a claim that filtering still exists.

## Recipes homepage screenshot — 2026-11-01

The Recipes placeholder is replaced with the reviewed actual homepage screenshot
from its own repository's `images/homepage-card.png`. The catalog uses the raw
GitHub URL for `image.url`, the corresponding GitHub file page for `image.source`,
and alt text and a caption explicitly describing a homepage screenshot.
The existing hosted-image validation accepts this owning-repository path;
no build or validation-rule changes were needed.

- In Recipes, `npm ci`, the Python build/content validation, the Node interaction
  tests, the capture script syntax check, and `git diff --check` passed.
- Playwright captured the current local homepage: heading, introduction, and all
  16 recipe links. Text bounds within `main.simple-index`, plus a 16-pixel inset,
  exclude the empty right side. The PNG is **1056 × 1300** pixels (2× density).
- Two successive captures produced identical SHA-256 hashes:
  `41fb08cb51562ffbdc75c300596ddc4c58599694c34baefaf9520a7e9ca9e32b`.
- An isolated temporary fixture with 40 recipes and longer wrapping titles
  captured successfully at **1702 × 4222** pixels. The script expanded its
  capture viewport past the initial desktop height and retained the full list.
  Fixture data is not part of either repository.
- In the index, `python3 scripts/build.py`, all **12** Python tests, and
  `git diff --check` passed. The build contains 12 listed projects and 12 public
  files; the hosted image is not copied into the deployment artifact. The new
  regression test verifies the reviewed URL/source, screenshot alt text,
  rendered image in place of a placeholder, and published catalog metadata.
- Chromium decoded and displayed the exact PNG in the Recipes card at 1280,
  768, 390, and 320 CSS pixels. The card fits each width. The existing introduction
  extends about 3 pixels beyond the viewport at 320 pixels; that separate layout
  issue is outside this card-image update. Desktop and mobile card screenshots
  were visually reviewed. No page JavaScript exceptions occurred.

The initial browser review above was local: it fulfilled the then-unpublished raw
image URL with the exact local PNG. Recipes commit `920b118` was subsequently
pushed before index commit `e0896ca`, and both deployments succeeded:
[Recipes workflow](https://github.com/rharriszzz/recipes/actions/runs/41372409076)
and [index workflow](https://github.com/rharriszzz/rharriszzz.github.io/actions/runs/41372442962).
The public raw PNG matched the reviewed SHA-256 hash, and all 30 external URLs
passed `python3 scripts/check_links.py`. Chromium then opened the live directory
and decoded the actual public 1056 × 1300 PNG in the Recipes card, without a
placeholder or request override.

For future refreshes, use the [project-image workflow](PROJECT_IMAGES.md) and the
Recipes repository's linked capture checklist. Refresh the source PNG after
homepage list/layout changes and publish it before any dependent index change.

## FFT Image Explorer illustration — 2026-11-01 (America/New_York)

The approved Candidate 5 card was merged into `fft-image-explorer/main`
at `ff513e6` before this index update. Source:
`docs/figures/local-fft-card.png` (1600 × 1000).
It is a computed composite from the original necklace photograph and its
Gaussian-windowed FFT, not an application screenshot.

The index references that specific owning-repository raw PNG, replaces the
neutral placeholder, and allows `docs/figures/` as a hosted-image directory
alongside `images/`. Regression checks verify the exact source URL, caption,
alt text, card rendering, and rejection of unapproved hosts or paths.
The source PNG and its generator remain in the FFT repository and are not
copied to index deployment artifacts.

This is a scoped figure integration, not a new repository-inventory review.
