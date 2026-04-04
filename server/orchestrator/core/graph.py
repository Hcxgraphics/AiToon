try:
    from langgraph.graph import END, StateGraph
except ModuleNotFoundError:  # pragma: no cover
    END = "__end__"
    StateGraph = None

from orchestrator.core.state import ComicState

from orchestrator.nodes.scene import scene_node
from orchestrator.nodes.character import character_node
from orchestrator.nodes.character_resolver import character_resolver_node
from orchestrator.nodes.dialogue import dialogue_node
from orchestrator.nodes.merge import merge_node

from orchestrator.validators.scene_validator import scene_validator
from orchestrator.validators.character_validator import character_validator
from orchestrator.validators.dialogue_validator import dialogue_validator


def _route_after_validation(state):
    if state.get("abort"):
        return "abort"
    return "next" if state.get("valid") else "retry"


class FallbackGraph:
    def invoke(self, state: ComicState):
        current_state = state

        # =========================
        # SCENE STAGE
        # =========================
        while True:
            current_state = scene_node(current_state)
            current_state = scene_validator(current_state)

            route = _route_after_validation(current_state)

            if route == "abort":
                return current_state

            if route == "retry":
                continue

            break

        # =========================
        # CHARACTER STAGE
        # =========================
        while True:
            current_state = character_node(current_state)
            current_state = character_validator(current_state)

            route = _route_after_validation(current_state)

            if route == "abort":
                return current_state

            if route == "retry":
                continue

            break

        # =========================
        # CHARACTER RESOLVER STAGE
        # =========================
        current_state = character_resolver_node(current_state)

        # =========================
        # DIALOGUE STAGE
        # =========================
        while True:
            current_state = dialogue_node(current_state)
            current_state = dialogue_validator(current_state)

            route = _route_after_validation(current_state)

            if route == "abort":
                return current_state

            if route == "retry":
                continue

            break

        # =========================
        # MERGE STAGE
        # =========================
        return merge_node(current_state)


if StateGraph is not None:
    builder = StateGraph(ComicState)

    # =========================
    # NODES
    # =========================
    builder.add_node("scene", scene_node)
    builder.add_node("scene_val", scene_validator)

    builder.add_node("character", character_node)
    builder.add_node("character_val", character_validator)

    builder.add_node("character_resolver", character_resolver_node)

    builder.add_node("dialogue", dialogue_node)
    builder.add_node("dialogue_val", dialogue_validator)

    builder.add_node("merge", merge_node)

    # =========================
    # ENTRY
    # =========================
    builder.set_entry_point("scene")

    # =========================
    # SCENE FLOW
    # =========================
    builder.add_edge("scene", "scene_val")

    builder.add_conditional_edges(
        "scene_val",
        _route_after_validation,
        {
            "retry": "scene",
            "next": "character",
            "abort": END,
        },
    )

    # =========================
    # CHARACTER FLOW
    # =========================
    builder.add_edge("character", "character_val")

    builder.add_conditional_edges(
        "character_val",
        _route_after_validation,
        {
            "retry": "character",
            "next": "character_resolver",
            "abort": END,
        },
    )

    # =========================
    # RESOLVER FLOW
    # =========================
    builder.add_edge("character_resolver", "dialogue")

    # =========================
    # DIALOGUE FLOW
    # =========================
    builder.add_edge("dialogue", "dialogue_val")

    builder.add_conditional_edges(
        "dialogue_val",
        _route_after_validation,
        {
            "retry": "dialogue",
            "next": "merge",
            "abort": END,
        },
    )

    # =========================
    # FINAL FLOW
    # =========================
    builder.add_edge("merge", END)

    graph = builder.compile()

else:
    graph = FallbackGraph()


def run_pipeline(user_input, llm_client=None, constraints_provider=None, user_id="test_user"):
    if constraints_provider is None:
        raise ValueError("constraints_provider is required")

    constraints = constraints_provider()

    initial_state: ComicState = {
        "prompt": user_input,
        "constraints": constraints,
        "llm_client": llm_client,

        "scene_data": [],
        "character_data": [],
        "dialogue_data": [],

        "valid": False,
        "abort": False,

        "scene_retries": 0,
        "character_retries": 0,
        "dialogue_retries": 0,

        "scene_error": None,
        "character_error": None,
        "dialogue_error": None,

        "user_id": user_id,
    }

    result = graph.invoke(initial_state)

    if result.get("abort"):
        raise ValueError(
            result.get(
                "fatal_error",
                "Pipeline aborted after validation retries"
            )
        )

    return result["final_output"]
