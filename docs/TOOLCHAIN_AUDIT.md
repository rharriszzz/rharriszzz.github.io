# Public repository toolchain maintenance

**Policy snapshot:** November 7, 2026. Check official lifecycle pages before
making later version decisions:
[Python](https://devguide.python.org/versions/),
[Node.js](https://nodejs.org/en/about/previous-releases),
[GitHub Actions](https://github.com/actions),
[Playwright](https://github.com/microsoft/playwright/releases).

## Scope and priority

Run the read-only scanner from this repository:

    python3 scripts/audit_toolchains.py > /tmp/rharriszzz-toolchains.md

It reads this repository's projects.json and audits **listed, public projects
(except HIS_profile)**, plus this central index and github-pages-discovery.
The latter receives website-level checks now because it may soon serve an
expanded public site. The command never reads the untestable HIS_profile repo.

For the remaining public repositories:

    python3 scripts/audit_toolchains.py --all-public > /tmp/all-public-toolchains.md

Use --all-indexed to include the projects.json entries deliberately hidden from
the landing page, without scanning every public repository. Use --format json
for machine-readable findings or --strict for a nonzero status on identified EOL
software in a website repository **or** incomplete audit coverage.

The script makes bounded, read-only GitHub requests and downloads selected
text files from public default branches. It cannot validate every transitive
dependency or prove runtime compatibility. A missing/oversized file or API
error is reported as incomplete coverage, never as a clean bill of health.

Unauthenticated GitHub API requests are rate-limited. With GitHub CLI already
authenticated, run in a private local shell:

    GH_TOKEN="$(gh auth token)" python3 scripts/audit_toolchains.py --strict

Do not put tokens in Markdown, logs, commits, or repository settings.

## Software policy

**For the public-facing website portion of every project:**

- No end-of-life software in builds, tests, or deployment. On this policy date,
  Python 3.10 and Node.js 20 are EOL. Python 3.11–3.13 receive only security fixes;
  prefer current bug-fix-maintained Python 3.14 or 3.15 for new setups. Node.js
  24 is an appropriate maintained LTS baseline, with 26 also available.
- Review outdated GitHub Actions major versions and migrate them to maintained
  releases, considering release notes and breaking changes. CI must be tested.
- Keep lockfiles, interpreter installations, browser test binaries, Docker
  images, and configuration references in sync. Never bump a Playwright package
  without addressing its browser image/version pairing.
- Verify build, tests, publication allowlists, and actual Pages deployment
  before reporting success. If a deployment fails, diagnose and repair it.
- Distinguish a library's declared *minimum compatibility* from recommending
  an obsolete interpreter as the preferred development environment.

**For non-website research:** current recommendations are still preferable,
but a necessary, isolated legacy environment may be retained while migration
is investigated. Preserve historical experiment evidence, provenance, and
old benchmark results accurately; do not silently rewrite their facts.

HIS_profile is excluded entirely because there is no longer a testable
environment. No audit result is a claim that it has been modernized.

## Repair workflow

1. Run the read-only audit; look at all findings and any incomplete coverage.
2. Inspect code and requirements before altering the recommended interpreter
   or dependency range. Check which components build public pages.
3. Change README/setup instructions and CI together where appropriate. For a
   public site, prefer an upgrade branch if its runtime behavior is uncertain.
4. Run suitable local/CI tests, and check the actual deployed website.
5. Record the changed paths, commit, and test evidence; rerun the audit.

This is an intentionally manual-review tool, not an automatic dependency
rewriter. Its maintenance snapshot and action-major table should themselves
be refreshed periodically.
