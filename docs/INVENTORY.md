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
| recipes | 2026-11-01 | Original; new static recipe collection | GitHub Pages recipe browser and print-friendly pages; production deployment documented | README, migration report, Pages workflow, production QA; typographic placeholder (no fabricated screenshot) |
| beads | 2026-11-01 | Original; curated pattern, geometry and photographic research; full archive retained on its research branch | https://rharriszzz.github.io/beads/ — GitHub Pages introduction and small pattern viewer; live desktop/mobile interactions verified | New README/topical docs, pinned source provenance, actual photo/R344/R345/R346 figures, separate R347 evidence epoch, standalone graph-paper code/tests, explicit publication allowlist; historical gallery retained |
| madweave | 2026-11-01 | Original; interactive JavaScript/SVG weaving app, with preserved historical material | GitHub Pages introduction, live editor, guide, and static SVG artwork export | New README, development/testing docs and improvement backlog; original SVG assets; browser-tested restoration fixes and artwork export |
| navier-stokes-vortex-lab | 2026-09-27 | Original; recent visualization and boundary-control research | No published site found; Pages disabled | README, STATUS.md, source tree, preview.png and rendering evidence; finite kinematic-model limits retained |
| navier-stokes-physical-approximation | 2026-09-10 | Original; recent numerical/physical research | No published site found; Pages disabled | README, source/config/test tree and committed baseline/reference plots; no accepted nonlinear core claimed |
| symphonium-disc-maker | 2026-10-02 | Original; recent geometry/fabrication experiment | No published site found; Pages disabled | README, source/test tree, pyproject, reference figures, prototype SVG; pending physical fit retained |
| fft-image-explorer | 2026-07-11 | Original; recent; interactive local Python image analysis | No published site found; Pages disabled | README, fft_image_explorer.py / scanner tree, requirements and input images; no application screenshot committed |
| bead_map | 2025-04-28 | Original; bead-detection experiments | No published site found; Pages disabled | No README; bead_map.py, bracelet-pattern-extractor.py and mask images |
| hsv_tools | 2025-04-26 | Original; image-analysis utilities | No published site found; Pages disabled | No README; hsv_picker.py, hsv_counts.py, requirements and masks |
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
physical disc. FFT Image Explorer has a neutral text panel rather than a
fabricated interface. Recipes likewise uses a typographic panel until a genuine
site screenshot is available.

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
