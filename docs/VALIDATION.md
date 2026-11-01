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
