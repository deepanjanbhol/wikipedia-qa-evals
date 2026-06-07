from __future__ import annotations

import unittest

from evals.utils import extract_json_object


class ExtractJsonObjectTests(unittest.TestCase):
    def test_extracts_plain_json_object(self) -> None:
        self.assertEqual(extract_json_object('{"answer": "Jane Austen", "score": 5}'), {"answer": "Jane Austen", "score": 5})

    def test_extracts_fenced_json_object(self) -> None:
        text = 'Here is the result:\n```json\n{"score": 4, "passed": true}\n```'
        self.assertEqual(extract_json_object(text), {"score": 4, "passed": True})

    def test_extracts_first_embedded_json_object(self) -> None:
        text = 'prefix {"failure_category": "Retrieval Failure"} suffix {"ignored": true}'
        self.assertEqual(extract_json_object(text), {"failure_category": "Retrieval Failure"})

    def test_returns_empty_dict_for_invalid_input(self) -> None:
        self.assertEqual(extract_json_object("not json"), {})


if __name__ == "__main__":
    unittest.main()