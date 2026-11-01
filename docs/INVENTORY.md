# Public repository review

Reviewed **2026-11-01** with the paginated GitHub public-user repositories API,
repository README/content/tree APIs, authenticated read-only Pages configuration
requests, HTTPS checks, and browser inspection. No other repository was modified.
The original API snapshots and local investigation files were kept outside this
checkout and are not part of the published artifact.

The inventory contained **17 public repositories**: eight selected projects,
eight secondary projects, and this central index. All 16 other public repositories
are included. No private repository names, data, or files are included. No repository
was marked archived in GitHub. “Historical” below describes age and context, not
GitHub’s archived flag or an assertion that the code is unsupported.

| Repository | Last push | Provenance / role | Verified website | Assets and evidence inspected |
| --- | --- | --- | --- | --- |
| reversi | 2026-11-01 | Original; recent; interactive browser game and coach | GitHub Pages; playable, engine responds after a move | README, index, Pages workflow/settings, public app, icon, research diagrams; fresh screenshot captured |
| arxiv-shelf | 2026-11-01 | Original; recent; local PDF library | GitHub Pages introduction; separately hosted browser edition may require permission | README, docs/index.html, public screenshot, workflow/settings; no catalog files copied |
| beads | 2026-10-21 | Original; recent geometry note in a historical photographic/render collection | None verified; Pages disabled | No README; beads.html, beads.pov, BEADS_POV_SINE_ANGLE.md, original reference photographs and rendered images |
| madweave | 2017-07-30 | Original; historical; interactive JavaScript/SVG weaving app | Documented fiberwoman.com host could not be verified; Pages disabled | README, index.html, MadWeaver.html, madweave.html, source tree, interface PNG and SVG assets |
| navier-stokes-vortex-lab | 2026-09-27 | Original; recent visualization and boundary-control research | No published site found; Pages disabled | README, STATUS.md, source tree, preview.png and rendering evidence; finite kinematic-model limits retained |
| navier-stokes-physical-approximation | 2026-09-10 | Original; recent numerical/physical research | No published site found; Pages disabled | README, source/config/test tree and committed baseline/reference plots; no accepted nonlinear core claimed |
| symphonium-disc-maker | 2026-10-02 | Original; recent geometry/fabrication experiment | No published site found; Pages disabled | README, source/test tree, pyproject, reference figures, prototype SVG; pending physical fit retained |
| fft-image-explorer | 2026-07-11 | Original; recent; interactive local Python image analysis | No published site found; Pages disabled | README, fft_image_explorer.py / scanner tree, requirements and input images; no application screenshot committed |
| bead_map | 2025-04-28 | Original; bead-detection experiments | No published site found; Pages disabled | No README; bead_map.py, bracelet-pattern-extractor.py and mask images |
| hsv_tools | 2025-04-26 | Original; image-analysis utilities | No published site found; Pages disabled | No README; hsv_picker.py, hsv_counts.py, requirements and masks |
| sound | 2017-07-30 | Original; historical Fourier/audio experiments | No published site found; Pages disabled | No README; test.c, fft.c, harmonics.c and plotting scripts |
| HIS_profile | 2020-06-22 | Original repository; historical Rocket Software / z/OS tooling | No published site found; Pages disabled | README, C/Python package and notebook tree, existing tree visualization; no ownership claim over employer code |
| zos_python | 2020-09-21 | Original repository; historical z/OS tooling | No published site found; Pages disabled | No README; setup.py, package initialization, system-service source/test tree |
| izODA.github.io | 2017-10-13 | Original repository; historical IBM documentation | Metadata homepage https://IzODA.github.io/ returns 404; account copy has Pages disabled | README, index.html and documentation/image tree; no internal IBM links copied to the index |
| numpy | 2019-03-14 | Fork; historical | Upstream homepage is not this fork’s live site; no live link offered | README and scientific package/build/test tree; no upstream branding copied |
| python-ibmdb | 2019-11-22 | Fork; historical | No fork website found; Pages disabled | README and IBM_DB driver/build/test tree |
| rharriszzz.github.io | 2026-11-01 | This index; empty public repository at task start | Pages already configured for Actions, with no previous homepage | No existing files or commits to overwrite; no separate card for the index itself |

The Madweave README names `http://fiberwoman.com/madweave/MadWeaver.html`.
Both HTTP and HTTPS probes returned HTTP 465 in this environment, so availability
could not be established. The index intentionally offers only the repository;
it does not claim the independent site is down. IzODA’s homepage is omitted
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
fabricated interface.

Supporting tools have compact text entries to keep the main directory readable.
Existing HIS Profile and image-mask figures were inspected but not copied into
the secondary collection. Historical forks retain explicit fork labels.

## Verification scope

The link checker verifies URLs and assets; manual app and responsive checks are
recorded in `docs/VALIDATION.md`. A current last-push timestamp is not evidence of
scientific validity. Descriptions intentionally omit unverified theorem claims,
hardware performance claims, and predictions about experiment success.
