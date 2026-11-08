import unittest

from scripts import audit_toolchains as tool


class ToolchainAuditTests(unittest.TestCase):
    def test_detects_end_of_life_site_runtimes(self):
        items = tool.analyze("README.md", "Requires Python 3.10+ and Node 20+", True)
        assert {x["rule"] for x in items} == {"eol-python", "eol-node"}
        self.assertTrue(all(x["severity"] == "error" for x in items))

    def test_maintained_versions_are_not_flagged(self):
        items = tool.analyze("README.md", "Python 3.15 and Node 24", True)
        self.assertEqual(items, [])

    def test_old_action_is_warning_not_automatic_change(self):
        items = tool.analyze(".github/workflows/pages.yml", "uses: actions/checkout@v4", True)
        self.assertEqual(items[0]["rule"], "older-action")

    def test_package_minimum_is_not_a_runtime_recommendation(self):
        items = tool.analyze("pyproject.toml", 'requires-python = ">=3.10"', True)
        self.assertEqual([x["rule"] for x in items], ["minimum-compatibility"])

    def test_index_scope_excludes_untestable_and_includes_future_website(self):
        repos = dict(tool.indexed())
        self.assertNotIn("HIS_profile", repos)
        self.assertNotIn("sound", repos)
        self.assertTrue(repos["github-pages-discovery"])
        self.assertTrue(repos["rharriszzz.github.io"])

    def test_candidate_scans_workflows_but_skips_snapshots(self):
        self.assertTrue(tool.candidate(".github/workflows/pages.yml"))
        self.assertTrue(tool.candidate("docs/PYTHON_ENVIRONMENT.md"))
        self.assertFalse(tool.candidate("docs/history/old_setup.md"))


if __name__ == "__main__":
    unittest.main()
