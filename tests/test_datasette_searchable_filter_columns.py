import unittest

from datasette_searchable_filter_columns import SCRIPT, extra_body_script


class SearchableFilterColumnsTests(unittest.TestCase):
    def test_script_targets_filter_column_selects(self):
        self.assertIn('select[name^="_filter_column"]', SCRIPT)
        self.assertIn("column-select-search", SCRIPT)

    def test_does_not_reorder_columns(self):
        # the plugin adds search only; it must not sort the column list
        self.assertNotIn("localeCompare", SCRIPT)
        self.assertNotIn("sortSelect", SCRIPT)

    def test_enabled_on_table_pages(self):
        self.assertEqual(SCRIPT, extra_body_script("table"))

    def test_disabled_elsewhere(self):
        self.assertIsNone(extra_body_script("query"))
        self.assertIsNone(extra_body_script("index"))


if __name__ == "__main__":
    unittest.main()
