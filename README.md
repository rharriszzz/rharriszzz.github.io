# Richard Harris — Projects

A central directory for the public software, mathematics, physics, visualization,
and experimental projects owned by `rharriszzz`.

**Website:** https://rharriszzz.github.io/

**Repository:** https://github.com/rharriszzz/rharriszzz.github.io

Individual applications and their websites remain in their own repositories.
This project deploys only the central directory. It does not change the Reversi
or arXiv Shelf deployments.

## Edit the collection

`projects.json` is the single source for project metadata. `index.template.html`
contains the page structure; `style.css` controls appearance. `scripts/build.py` renders a complete static page into
`dist/`, including all listed project links. The directory has one ordered project grid,
without JavaScript, search, or category filters. It does not call GitHub’s API at runtime.

To change a description, edit its `description`, `kind`, `technology`, and
optional `note` fields. Keep scientific limitations explicit. All listed projects use the same card layout; the order of entries in `projects.json`
determines display order. Put the most interesting projects first.

Set `listed: false` on an entry to exclude it from the website, search, counts,
public JSON catalog, and deployed assets without deleting its source metadata.
Omit the property (or use `true`) to list a project again. Historical projects
are included selectively: HIS Profile remains listed; Sound, z/OS Python,
IzODA documentation, and the NumPy fork are currently unlisted.
Sound can be restored if the project becomes interesting again.
Deleted repositories should be removed from `projects.json`, not retained as
unlisted entries; the deleted Python IBM DB fork was removed accordingly.

To add a project:

1. Confirm it is a **public repository owned by `rharriszzz`**. Inspect its README,
   source, Pages settings, and any independently hosted site.
2. Add an entry to `projects.json`. Copy the field structure of a similar entry;
   use the repository’s exact name for `slug`, and record its public URL, fork
   status, archived status, default branch, and last push date in `repository`.
3. Choose one or more categories: `games`, `research`, `visualization`, `craft`,
   or `tools`. Set `browserApp` only for an actual browser application. A local
   Matplotlib interface is a local app. An explanatory website is an introduction.
4. Add `site` only after opening and exercising the actual public page. Its
   `detail` should identify the page type and hosting provider. Omit `site`
   entirely when a working public website cannot be verified; the repository
   link is always present. Do not add private application or dataset links.
5. Update `verifiedOn` after a full inventory/link review, run the checks below,
   and update `docs/INVENTORY.md` when coverage or publication status changes.

### Images

Place reviewed local project images in `assets/images/`. Add an `image` object with
`path`, meaningful `alt` text, a factual `caption`, and the public `source` URL.
Use actual project screenshots, renders, plots, or photographs. Keep screenshots
free of browser chrome, local paths, personal files, tokens, and private data.
Check licensing and attribution before copying third-party material.

Local images in this index are unmodified copies of public repository assets, except
the Reversi screenshot, which was captured from its public app after a real move.
Their source locations are recorded in the catalog and [asset notes](docs/INVENTORY.md).
The arXiv Shelf image was already published on its public landing page; no local
catalog or PDF collection is copied here. FFT Image Explorer uses a
computed composite of the original necklace photograph and its actual
Gaussian-windowed 2D FFT, generated reproducibly in that repository.
It is a scientific illustration, **not** an application screenshot.

Removing an image from an entry also removes it from the next published build.
Only referenced local images are copied. SVGs must be self-contained static drawings.
The HIS Profile, Recipes, and FFT Image Explorer cards instead display images
from their original public GitHub repositories via `image.url`, with explicit
source links and captions.
Recipes uses the reviewed `images/homepage-card.png`, an actual homepage screenshot
of the heading, introduction, and complete recipe list, cropped to exclude the
empty right side. Regenerate it in the Recipes repository using its documented
`npm run capture:homepage-card` command when that homepage changes.
Hosted image URLs are restricted to `images/` or `docs/figures/` in the
owning project's GitHub raw-content path. These images are not copied into
the Pages artifact.

Follow the [project-image workflow](docs/PROJECT_IMAGES.md) for future screenshot
refreshes, including the Recipes capture instructions, review checks, source-first
push order, and live-site verification. Refreshing the same hosted PNG usually
needs only a commit in its source repository.

## Build, test, and preview

Requires Python 3.10+. No third-party Python packages, npm installation,
framework, or package lockfile are needed.

```sh
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 scripts/check_links.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:8000/ and check the desktop layout, a tablet width, and an
iPhone width (including 320 CSS pixels). Check the card order, images, links,
and keyboard focus. No JavaScript, analytics, third-party fonts, tracking scripts,
cookies, or runtime API requests are used by this site.

The standard-library tests check catalog coverage, escaping, private-entry
rejection, image/anchor paths, basic accessibility markup, and the exact set of
files allowed in the deployment artifact. They do not replace visual browser QA.
`check_links.py` performs actual HTTPS GET requests for every external page in
the generated HTML and every public image-provenance link. A successful response
does not establish application functionality; live apps also need manual checks.

After publishing, verify all linked assets and the catalog on the live host:

```sh
python3 scripts/check_links.py --base-url https://rharriszzz.github.io/
```

## Deployment

The public repository uses branch `main` and **Settings → Pages → Source: GitHub
Actions**. `.github/workflows/pages.yml` validates every push and pull request,
uploads only `dist/`, and deploys successful `main` builds to the production URL.
Pull requests run checks without deploying. A manual workflow dispatch is also
available. External link checks are deliberate maintenance commands rather than
mandatory deployment gates, so a temporary third-party outage cannot prevent a
catalog correction from shipping.

`dist/` is generated and ignored by Git. The build uses an explicit file allowlist:
the rendered HTML, CSS, JavaScript, favicon, reviewed JSON catalog, `.nojekyll`,
and images referenced by the catalog. It does **not** publish the checkout,
README, audit documents, scripts, tests, `.git`, or arbitrary files in `assets/`.
It does not fetch files from other checkouts or call GitHub during a build.

Commit and push source changes to publish:

```sh
git add projects.json assets/images
git commit -m "Update project collection"
git push origin main
gh run list --workflow pages.yml
```

## Maintenance

An occasional manual review is sufficient. There is no recurring process or
runtime API dependency. To discover new public repositories without listing
private repositories:

```sh
gh api 'users/rharriszzz/repos?type=owner&per_page=100' --paginate \
  --jq '.[] | select(.private == false) | {name, fork, archived, pushed_at, has_pages, homepage}'
```

Compare the results with `projects.json`; inspect new or changed projects before
adding them. `has_pages` and `homepage` are clues, not evidence that a site works.
Use `gh api repos/rharriszzz/REPOSITORY/pages` to inspect Pages configuration and
visit the actual returned URL. Record reachability limits honestly. Historical
repositories are not necessarily marked archived in GitHub; a last-push date is
context, not a promise of ongoing maintenance.
