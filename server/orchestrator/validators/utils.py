MAX_RETRIES = 2


def pass_validation(state, error_key: str):
    return {
        **state,
        "valid": True,
        "abort": False,
        error_key: None,
    }


def fail_validation(state, retry_key: str, error_key: str, message: str):
    retries = state.get(retry_key, 0)
    next_retries = retries + 1

    next_state = {
        **state,
        "valid": False,
        error_key: message,
        retry_key: next_retries,
    }

    if next_retries >= MAX_RETRIES:
        next_state["abort"] = True
        next_state["fatal_error"] = f"{error_key}: {message}"

    return next_state
