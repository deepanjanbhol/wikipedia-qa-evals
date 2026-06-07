from __future__ import annotations

import unittest

from evals.rule_metrics import abstention_consistency, abstention_triggered, page_hit_at_k, search_count


class RuleMetricTests(unittest.TestCase):
    def test_page_hit_matches_normalized_titles_and_urls(self) -> None:
        self.assertTrue(
            page_hit_at_k(
                retrieved_titles=["https://en.wikipedia.org/wiki/Pride_and_Prejudice"],
                expected_pages=["pride and prejudice"],
            )
        )

    def test_page_hit_returns_false_without_overlap(self) -> None:
        self.assertFalse(page_hit_at_k(retrieved_titles=["K2"], expected_pages=["Mount Everest"]))

    def test_abstention_triggered_is_lexical_and_case_insensitive(self) -> None:
        self.assertTrue(abstention_triggered("I CANNOT DETERMINE that from the retrieved evidence."))

    def test_empty_answer_counts_as_abstention(self) -> None:
        self.assertTrue(abstention_triggered("   "))

    def test_abstention_consistency_matches_expected_behavior(self) -> None:
        self.assertTrue(abstention_consistency(True, "There is insufficient evidence."))
        self.assertTrue(abstention_consistency(False, "Jane Austen wrote Pride and Prejudice."))

    def test_search_count_ignores_empty_and_non_string_queries(self) -> None:
        self.assertEqual(search_count(["Marie Curie", "", "  ", None, "Poland"]), 2)


if __name__ == "__main__":
    unittest.main()