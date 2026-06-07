from __future__ import annotations

import unittest

from agent.prompt import DEFAULT_PROMPT_VERSION, get_prompt, list_prompt_versions, resolve_prompt_version


class PromptVersionTests(unittest.TestCase):
    def test_resolves_short_aliases(self) -> None:
        self.assertEqual(resolve_prompt_version("v0"), "v0_base")
        self.assertEqual(resolve_prompt_version("v1"), "v1_advanced")
        self.assertEqual(resolve_prompt_version("v2"), "v2_rai_guarded")

    def test_unknown_version_falls_back_to_default(self) -> None:
        self.assertEqual(resolve_prompt_version("does_not_exist"), DEFAULT_PROMPT_VERSION)

    def test_get_prompt_includes_version_and_final_json_contract(self) -> None:
        prompt = get_prompt("v2")
        self.assertIn("Prompt Version: v2_rai_guarded", prompt)
        self.assertIn("Your final message must be ONLY valid JSON", prompt)
        self.assertIn("search_wikipedia", prompt)

    def test_list_prompt_versions_contains_all_canonical_versions(self) -> None:
        self.assertEqual(set(list_prompt_versions()), {"v0_base", "v1_advanced", "v2_rai_guarded"})


if __name__ == "__main__":
    unittest.main()