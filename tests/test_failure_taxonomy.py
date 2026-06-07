from __future__ import annotations

import unittest

from evals.failure_taxonomy import classify_failure


class FailureTaxonomyTests(unittest.TestCase):
    def test_classifies_clear_no_failure(self) -> None:
        result = classify_failure(
            slice_name="simple_factoid",
            should_abstain=False,
            page_hit=True,
            abstention_triggered=False,
            searches_used=["Pride and Prejudice author"],
            faithfulness={"score": 5},
            answer_relevancy={"score": 5},
            context_precision={"score": 5},
            context_recall={"score": 5},
            correctness={"score": 5},
            completeness={"score": 5},
            citation_support={"score": 5},
            abstention_quality={"passed": True},
            use_claude_tiebreak=False,
        )
        self.assertEqual(result["failure_category"], "No Failure")

    def test_tag_breaks_tie_for_ambiguous_abstention_failure(self) -> None:
        result = classify_failure(
            slice_name="ambiguous",
            tags=["Ambiguity Failure"],
            should_abstain=True,
            page_hit=True,
            abstention_triggered=False,
            searches_used=["Washington", "George Washington"],
            faithfulness={"score": 4},
            answer_relevancy={"score": 4},
            context_precision={"score": 4},
            context_recall={"score": 4},
            correctness={"score": 3},
            completeness={"score": 3},
            citation_support={"score": 4},
            abstention_quality={"passed": False},
            use_claude_tiebreak=False,
        )
        self.assertEqual(result["failure_category"], "Ambiguity Failure")

    def test_classifies_retrieval_failure_when_page_missed_and_context_weak(self) -> None:
        result = classify_failure(
            slice_name="multi_hop",
            should_abstain=False,
            page_hit=False,
            abstention_triggered=False,
            searches_used=["penicillin discoverer"],
            context_precision={"score": 2},
            context_recall={"score": 2},
            correctness={"score": 4},
            completeness={"score": 4},
            faithfulness={"score": 4},
            citation_support={"score": 4},
            abstention_quality={"passed": True},
            use_claude_tiebreak=False,
        )
        self.assertEqual(result["failure_category"], "Retrieval Failure")


if __name__ == "__main__":
    unittest.main()