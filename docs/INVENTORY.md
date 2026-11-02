# Public repository review

Reviewed **2026-11-01** with the paginated GitHub public-user repositories API,
repository README/content/tree APIs, authenticated read-only Pages configuration
requests, HTTPS checks, and browser inspection. No other repository was modified.
The original API snapshots and local investigation files were kept outside this
checkout and are not part of the published artifact.

The current index source describes **17 repositories**: 12 projects in a single
ordered directory, four editorially unlisted historical projects, and this
central index. All 16 other retained repositories remain documented here,
but only 12 are currently shown on the index website. No private repository names, data, or files are included. No repository
was marked archived in GitHub. “Historical” below describes age and context, not
GitHub’s archived flag or an assertion that the code is unsupported.

| Repository | Last push | Provenance / role | Verified website | Assets and evidence inspected |
| --- | --- | --- | --- | --- |
| reversi | 2026-11-01 | Original; recent; interactive browser game and coach | GitHub Pages; playable, engine responds after a move | README, index, Pages workflow/settings, public app, icon, research diagrams; fresh screenshot captured |
| arxiv-shelf | 2026-11-01 | Original; recent; local PDF library | GitHub Pages introduction; separately hosted browser edition may require permission | README, docs/index.html, public screenshot, workflow/settings; no catalog files copied |
| recipes | 2026-11-01 | Original; new static recipe collection | GitHub Pages recipe browser and print-friendly pages; production deployment documented | README, migration report, Pages workflow, production QA; reviewed actual homepage screenshot and reproducible Playwright capture script |
| beads | 2026-11-01 | Original; curated pattern, geometry and photographic research; full archive retained on its research branch | https://rharriszzz.github.io/beads/ — GitHub Pages introduction and small pattern viewer; live desktop/mobile interactions verified | New README/topical docs, pinned source provenance, actual photo/R344/R345/R346 figures, separate R347 evidence epoch, standalone graph-paper code/tests, explicit publication allowlist; historical gallery retained |
| madweave | 2026-11-01 | Original; interactive JavaScript/SVG weaving app, with preserved historical material | GitHub Pages introduction, live editor, guide, and static SVG artwork export | New README, development/testing docs and improvement backlog; original SVG assets; browser-tested restoration fixes and artwork export |
| navier-stokes-vortex-lab | 2026-09-27 | Original; recent visualization and boundary-control research | No published site found; Pages disabled | README, STATUS.md, source tree, preview.png and rendering evidence; finite kinematic-model limits retained |
| navier-stokes-physical-approximation | 2026-09-10 | Original; recent numerical/physical research | No published site found; Pages disabled | README, source/config/test tree and committed baseline/reference plots; no accepted nonlinear core claimed |
| symphonium-disc-maker | 2026-10-02 | Original; recent geometry/fabrication experiment | No published site found; Pages disabled | README, source/test tree, pyproject, reference figures, prototype SVG; pending physical fit retained |
| fft-image-explorer | 2026-11-02 | Original; interactive local Python image analysis | No published site found; Pages disabled | README, Gaussian FFT figure generator and numerical tests, original necklace and saved centerline; reviewed Candidate 5 scientific figure (not an app screenshot) |
| bead_map | 2026-11-02 | Original; bead-detection and photographic-mask experiments | No published site found; Pages disabled | README, Python image-analysis scripts, original mask images and reproducible two-panel illustration in docs/figures |
| hsv_tools | 2026-11-02 | Original; interactive HSV selection and pixel-count utilities | No published site found; Pages disabled | README, actual HSV Picker mask illustration, histogram figure, reproducible generator, tests, original photo and masks |
| sound | 2017-07-30 | Original; historical Fourier/audio experiments | No published site found; Pages disabled | No README; test.c, fft.c, harmonics.c and plotting scripts |
| HIS_profile | 2020-06-22 | Original repository; historical Rocket Software / z/OS tooling | No published site found; Pages disabled | README, C/Python package, notebook tree, and published `images/Tree.jpg` Bokeh radial profiling example; no ownership claim over employer code |
| zos_python | 2020-09-21 | Original repository; historical z/OS tooling | No published site found; Pages disabled | No README; setup.py, package initialization, system-service source/test tree |
| izODA.github.io | 2017-10-13 | Original repository; historical IBM documentation | Metadata homepage https://IzODA.github.io/ returns 404; account copy has Pages disabled | README, index.html and documentation/image tree; no internal IBM links copied to the index |
| numpy | 2019-03-14 | Fork; historical | Upstream homepage is not this fork’s live site; no live link offered | README and scientific package/build/test tree; no upstream branding copied |
| rharriszzz.github.io | 2026-11-01 | This index; empty public repository at task start | Pages already configured for Actions, with no previous homepage | No existing files or commits to overwrite; no separate card for the index itself |

The Madweave README names `http://fiberwoman.com/madweave/MadWeaver.html`.
Both HTTP and HTTPS probes returned HTTP 465 in this environment, so availability
could not be established. The updated entry links to the newly verified GitHub Pages site;
it does not claim the independent historical site is down. IzODA’s homepage is omitted
because the actual GET returned 404. NumPy’s upstream site is not presented as
a personal project deployment.

## Image provenance

Every `image.source` in `projects.json` identifies the public origin. Assets are
copied without visual alterations. The Reversi screenshot contains only the
public app viewport, captured after Black D3 and the computer’s White C5 reply;
it contains no browser toolbar, account information, or local filesystem paths.

The arXiv Shelf screenshot comes from the already public `docs/assets/` landing
page asset, not from a private local library. It is labeled as a browser-edition
screenshot, not as the public introduction’s UI. Beads uses an original input
photograph. Madweave uses its committed interface image. Vortex Lab uses its
committed illustrative tank preview. Physical Approximation uses the published
explicit comparison plot, whose title states that nonlinear core corrections
are omitted. Symphonium uses its generated sampler SVG, not a photo of a tested
physical disc. FFT Image Explorer uses a computed two-panel scientific
illustration from its original necklace photograph and actual Gaussian-windowed
2D FFT, not an application screenshot. Recipes embeds its reviewed actual
homepage screenshot from
[`images/homepage-card.png`](https://github.com/rharriszzz/recipes/blob/main/images/homepage-card.png).
The Recipes repository's `scripts/capture_homepage_card.mjs` rebuilds and serves
the current homepage, then measures the text in `main.simple-index` to capture
the title, introduction, and complete recipe list without the empty right side.
Its README documents regeneration and refreshing the image after list/layout
changes. The index references the original PNG through `image.url`; no copy is
stored here.

Supporting tools appear toward the end of the same card grid. The only
listed historical repository is HIS Profile. Sound, z/OS Python, IzODA
documentation, and the NumPy fork are intentionally unlisted,
but retain their metadata in source control. Sound may be restored later.
The Python IBM DB fork was deleted from GitHub by its owner and was removed
from this source catalog; the original 2026-11-01 review is historical. The
published projects.json contains listed entries only.
The HIS Profile card embeds the authentic public `images/Tree.jpg` from its
own repository without copying it into the index; image-mask figures were
inspected but not copied into the index. Historical forks retain explicit fork labels.

### FFT Image Explorer — 2026-11-01 illustration

The selected [Candidate 5 two-panel figure](https://github.com/rharriszzz/fft-image-explorer/blob/main/docs/figures/local-fft-card.png)
is a **1600 × 1000 computed illustration**, not an application screenshot.
The left panel shows the original necklace, a selected centerline point, and
Gaussian contours; the right panel shows the corresponding actual 2D FFT.
The card references `docs/figures/local-fft-card.png` from the FFT repository
directly, with provenance in `projects.json`. The index does not copy it.

The FFT repository contains a reproducible
[figure-generation script](https://github.com/rharriszzz/fft-image-explorer/blob/main/scripts/generate_fft_figures.py),
numerical tests and
[figure documentation](https://github.com/rharriszzz/fft-image-explorer/blob/main/docs/fft-figures.md).
Regenerate and review the figure in that repository when refreshing it here.

### Bead Map — 2026-11-01 card image

The owner selected the [two-panel bead-map illustration](https://github.com/rharriszzz/bead_map/blob/main/docs/figures/bead-map-card.png).
It juxtaposes an actual cropped necklace photograph and the same crop of the
existing hand-selected yellow, red and black masks, recolored to show their
respective categories. It is an illustration of intermediate mask results,
not a claim of validated bead-center identification or a completed sequence.

The Bead Map repository owns the source 1200 × 660 PNG, its
[generator](https://github.com/rharriszzz/bead_map/blob/main/scripts/generate_bead_map_figures.py),
400 × 220 preview, candidate sheet, and
[README instructions](https://github.com/rharriszzz/bead_map/blob/main/README.md).
The central index embeds its main-branch image URL rather than copying it into
the deployment artifact.

### HSV Tools — 2026-11-01 card illustration

The [two-panel HSV Picker figure](https://github.com/rharriszzz/hsv_tools/blob/main/docs/figures/hsv-tools-card.png)
shows a crop of the original necklace photograph with a real sampling line
on a red bead, alongside the actual black-on-white HSV match mask generated
from that line. This is a computed composition based on the tool's algorithm,
not a screenshot of the running interactive window or a completed bead map.

The HSV Tools repository owns the 1600 × 1000 figure, its 400 × 250 preview,
the independent color-count histogram, mask outputs and a reproducible
[generator](https://github.com/rharriszzz/hsv_tools/blob/main/scripts/generate_hsv_figures.py).
Its [README](https://github.com/rharriszzz/hsv_tools/blob/main/README.md) and
[figure notes](https://github.com/rharriszzz/hsv_tools/blob/main/docs/figures.md)
record the source photograph, exact sample coordinates, tolerance settings and
checks. The central directory references the source image rather than
duplicating it.

## Verification scope

The Beads entry was updated separately on 2026-11-01 after its curated site was
published. Its production build/deploy completed successfully. Live browser checks
covered desktop, tablet, 390px and 320px widths, both evidence epochs, strict and
provisional masks, source lists, selection, zoom, keyboard access, image loading,
the original gallery and JavaScript-disabled content. The candidate remains
conditional: 201 supported / 0 conflicting / 7 insufficient, with 1040/1040
retained-label agreement, is not independent chart/object validation. The existing
index photograph and all other catalog entries remain unchanged. This scoped
follow-up is not a new full review of the other repositories.

The MadWeave entry was updated separately on 2026-11-01 after its project site
was deployed and exercised in Chromium. The follow-up covers the landing page,
user guide, embedded SVG editor, pattern/size/spacing controls, and static artwork
export. The existing authentic interface image is retained. The description
now includes complete offline editable project saving and original SVG import,
and keeps the original editor's mouse/trackpad limitation visible. This scoped
follow-up does not re-review unrelated projects.

The link checker verifies URLs and assets; manual app and responsive checks are
recorded in `docs/VALIDATION.md`. A current last-push timestamp is not evidence of
scientific validity. Descriptions intentionally omit unverified theorem claims,
hardware performance claims, and predictions about experiment success.
