from typing import Any, Dict, List, Optional, TypedDict


class ComicState(TypedDict, total=False):
    prompt: str
    constraints: Dict[str, List[str]]
    llm_client: Any

    scene_data: List[Dict[str, Any]]
    character_data: List[Dict[str, Any]]
    dialogue_data: List[Dict[str, Any]]
    final_output: Dict[str, Any]

    valid: bool
    abort: bool
    fatal_error: Optional[str]

    scene_retries: int
    character_retries: int
    dialogue_retries: int

    scene_error: Optional[str]
    character_error: Optional[str]
    dialogue_error: Optional[str]
