from orchestrator.core.graph import run_pipeline


def test_orchestrator():
    prompt = """
A brave warrior enters a dark forest and encounters a mysterious shadow creature.
"""

    constraints = {
        "themes": ["Fantasy", "Dark", "Adventure"],
        "bubble_types": ["Speech: oval", "Thought: cloud"]
    }

    result = run_pipeline(
        user_input=prompt,
        constraints_provider=lambda: constraints,
        user_id="test_user"
    )

    print("\n FINAL OUTPUT:\n")
    print(result)


if __name__ == "__main__":
    test_orchestrator()