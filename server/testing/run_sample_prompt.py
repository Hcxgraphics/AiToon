import argparse
import json
import sys
from pathlib import Path


SERVER_ROOT = Path(__file__).resolve().parents[1]
if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

from services.ai_service import run_orchestrator


DEFAULT_PROMPT = 'A pink hair cute girl found a unicorn on an island named "Kolinda".'
DEFAULT_THEME = "Fantasy"


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AiToon orchestrator on a sample prompt.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Prompt to send to the orchestrator.")
    parser.add_argument("--theme", default=DEFAULT_THEME, help="Theme to send to the orchestrator.")
    args = parser.parse_args()

    result = run_orchestrator(args.prompt, args.theme , user_id="test_user")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
