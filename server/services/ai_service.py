from services.workflows import StarterWorkflowService

_starter_workflow_service = StarterWorkflowService()


def run_orchestrator(prompt, theme, user_id="test_user"):
    return _starter_workflow_service.run_orchestrator(prompt=prompt, theme=theme, user_id=user_id)


def generate_comic_package(prompt, theme, user_id="test_user"):
    return _starter_workflow_service.create_package_from_prompt(
        prompt=prompt,
        theme=theme,
        user_id=user_id,
    )
