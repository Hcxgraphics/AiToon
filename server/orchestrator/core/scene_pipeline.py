from orchestrator.agents.scene_agent import SceneAgent
from orchestrator.agents.dialogue_agent import DialogueAgent
from orchestrator.validators.scene_validator import validate_scenes

def run_scene_pipeline(data):
    state = {}

    scene_agent = SceneAgent()
    scenes = scene_agent.generate(data)

    dialogue_agent = DialogueAgent()
    scenes = dialogue_agent.enhance(scenes, data)

    validated_scenes = validate_scenes(scenes)

    return validated_scenes