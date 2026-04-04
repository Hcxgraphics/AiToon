import json
import sys
import unittest
from pathlib import Path


SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from orchestrator.agents.llm import FALLBACK_MODEL, PRIMARY_MODEL, SECONDARY_MODEL, RoutedLLM, route_request
from orchestrator.core.graph import run_pipeline
from orchestrator.schema.validator import validate_master


class DemoLLM:
    def __init__(self):
        self.dialogue_calls = 0

    def generate(self, prompt: str, max_new_tokens: int = 1024, task_type: str = "fast_agent") -> str:
        if "Scene Generator" in prompt:
            return json.dumps(
                [
                    {
                        "panel_id": 1,
                        "theme": "Cyberpunk",
                        "scene_description": "Loid walks through a neon alley under heavy rain.",
                        "location": "Neon alley",
                        "time": "Night",
                        "camera_angle": "Wide shot",
                        "action": "Loid scans the street",
                        "emotion": "Serious",
                    },
                    {
                        "panel_id": 2,
                        "theme": "Cyberpunk",
                        "scene_description": "Loid stops beneath a holographic sign and speaks.",
                        "location": "Market overpass",
                        "time": "Night",
                        "camera_angle": "Medium close-up",
                        "action": "Loid speaks into the rain",
                        "emotion": "Serious",
                    },
                ]
            )
        if "Character Generator" in prompt:
            return json.dumps(
                [
                    {
                        "panel_id": 1,
                        "characters": [
                            {
                                "char_id": "c1",
                                "name": "Loid",
                                "appearance": "Tall spy in a dark cyberpunk trench coat",
                                "emotion": "Serious",
                                "pose": "Walking cautiously",
                            }
                        ],
                    },
                    {
                        "panel_id": 2,
                        "characters": [
                            {
                                "char_id": "c1",
                                "name": "Loid",
                                "appearance": "Tall spy in a dark cyberpunk trench coat",
                                "emotion": "Serious",
                                "pose": "Walking cautiously",
                            }
                        ],
                    },
                ]
            )

        self.dialogue_calls += 1
        if self.dialogue_calls == 1:
            return json.dumps(
                [
                    {
                        "panel_id": 1,
                        "dialogues": [
                            {
                                "char_id": "c1",
                                "text": "This city never sleeps.",
                                "tone": "serious",
                                "bubble_type": "InvalidBubble",
                                "position_hint": "left",
                            }
                        ],
                        "narration": "Rain hisses off the metal road.",
                    },
                    {
                        "panel_id": 2,
                        "dialogues": [
                            {
                                "char_id": "c1",
                                "text": "Stay focused.",
                                "tone": "serious",
                                "bubble_type": "Speech: oval",
                                "position_hint": "right",
                            }
                        ],
                        "narration": "A drone hums overhead.",
                    },
                ]
            )

        return json.dumps(
            [
                {
                    "panel_id": 1,
                    "dialogues": [
                        {
                            "char_id": "c1",
                            "text": "This city never sleeps.",
                            "tone": "serious",
                            "bubble_type": "Speech: oval",
                            "position_hint": "left",
                        }
                    ],
                    "narration": "Rain hisses off the metal road.",
                },
                {
                    "panel_id": 2,
                    "dialogues": [
                        {
                            "char_id": "c1",
                            "text": "Stay focused.",
                            "tone": "serious",
                            "bubble_type": "Speech: rectangle",
                            "position_hint": "right",
                        }
                    ],
                    "narration": "A drone hums overhead.",
                },
            ]
        )


def demo_constraints():
    return {
        "themes": ["Cyberpunk", "Anime"],
        "bubble_types": ["Speech: oval", "Speech: rectangle", "Thought"],
    }


class PipelineTestCase(unittest.TestCase):
    def test_pipeline_retries_only_failed_dialogue_stage(self):
        fake_llm = DemoLLM()

        output = run_pipeline(
            "Cyberpunk night scene with Loid speaking seriously",
            llm_client=fake_llm,
            constraints_provider=demo_constraints,
        )

        self.assertEqual(fake_llm.dialogue_calls, 2)
        self.assertEqual(len(output["panels"]), 2)
        self.assertEqual([panel["panel_id"] for panel in output["panels"]], [1, 2])

        for panel in output["panels"]:
            self.assertIn(panel["theme"], demo_constraints()["themes"])
            for dialogue in panel["dialogues"]:
                self.assertIn(dialogue["bubble_type"], demo_constraints()["bubble_types"])

        is_valid, error = validate_master(output)
        self.assertTrue(is_valid, error)


class StubProvider:
    def __init__(self, responses=None, error=None):
        self.responses = list(responses or [])
        self.error = error
        self.calls = []

    def generate(self, prompt: str, max_new_tokens: int = 1024) -> str:
        self.calls.append(prompt)
        if self.error is not None:
            raise self.error
        if self.responses:
            return self.responses.pop(0)
        return json.dumps({"ok": True})


class RoutingTestCase(unittest.TestCase):
    def test_route_request_returns_expected_primary_provider(self):
        self.assertEqual(route_request("fast_agent"), PRIMARY_MODEL)
        self.assertEqual(route_request("long_story"), SECONDARY_MODEL)
        self.assertEqual(route_request("fallback"), FALLBACK_MODEL)

    def test_routed_llm_falls_back_after_rate_limit(self):
        routed_llm = RoutedLLM()
        groq_provider = StubProvider(error=RuntimeError("429 rate limit exceeded"))
        gemini_provider = StubProvider(responses=['{"provider":"gemini"}'])
        openrouter_provider = StubProvider(responses=['{"provider":"openrouter"}'])
        routed_llm.providers = {
            PRIMARY_MODEL: groq_provider,
            SECONDARY_MODEL: gemini_provider,
            FALLBACK_MODEL: openrouter_provider,
        }

        response = routed_llm.generate("{}", task_type="fast_agent")

        self.assertEqual(json.loads(response)["provider"], "gemini")
        self.assertEqual(len(groq_provider.calls), 1)
        self.assertEqual(len(gemini_provider.calls), 1)
        self.assertEqual(len(openrouter_provider.calls), 0)

    def test_routed_llm_uses_openrouter_after_secondary_failure(self):
        routed_llm = RoutedLLM()
        groq_provider = StubProvider(responses=['{"provider":"groq"}'])
        gemini_provider = StubProvider(error=RuntimeError("Gemini crashed"))
        openrouter_provider = StubProvider(responses=['{"provider":"openrouter"}'])
        routed_llm.providers = {
            PRIMARY_MODEL: groq_provider,
            SECONDARY_MODEL: gemini_provider,
            FALLBACK_MODEL: openrouter_provider,
        }

        response = routed_llm.generate("{}", task_type="long_story")

        self.assertEqual(json.loads(response)["provider"], "openrouter")
        self.assertEqual(len(gemini_provider.calls), 1)
        self.assertEqual(len(groq_provider.calls), 0)
        self.assertEqual(len(openrouter_provider.calls), 1)


if __name__ == "__main__":
    unittest.main()
