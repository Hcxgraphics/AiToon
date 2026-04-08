from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from groq import Groq
from orchestrator.logger import get_logger
from config.db import get_db
from services.ai_service import run_orchestrator

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
logger = get_logger("routes.ai")

class SuggestRequest(BaseModel):
    type: str   # storyline / tagline / summary
    context: str
    characters: Optional[List[str]] = [] 


class GenerateRequest(BaseModel):
    project_id: str
    storyline: str
    summary: Optional[str] = ""
    characters: Optional[List[dict]] = []
    theme: Optional[str] = None  

def format_characters(chars):
    if not chars:
        return "No characters provided"
    
    text = ""
    for c in chars:
        if isinstance(c, str):
            text += f"\n- {c}"
        else:
            text += f"""
- Name: {c.get('name')}
  Personality: {c.get('personality')}
  Style: {c.get('style')}
  Appearance: {c.get('appearance')}
"""
    return text



@router.post("/ai/suggest")
def suggest(data: SuggestRequest):
    
    char_context = format_characters(data.characters)

    prompt = f"""
        You are an AI Comic Writer.

STRICT RULES:
- You MUST use ONLY the provided characters
- DO NOT invent new characters
- DO NOT rename characters
- DO NOT introduce extra characters

CHARACTERS:
{char_context}

TASK:
Generate a {data.type} for a comic story.

CONTEXT:
{data.context}

STYLE:
- Engaging
- Creative
- Cinematic

IMPORTANT:
- Use EXACT character names given above
- Every main character must be from the list
- If you introduce any new character, the output is INVALID

OUTPUT:
Return only the {data.type}.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "suggestion": response.choices[0].message.content
    }

@router.post("/generate")
def generate(data: GenerateRequest):
    try:
        db = get_db()

        prompt = f"""
        Storyline: {data.storyline}
        Summary: {data.summary}
        """

        result = run_orchestrator(prompt , data.theme)

        final_output = result["final_output"]
        debug_data = result.get("debug", {})

        db.projects.update_one(
            {"_id": data.project_id},
            {
                "$set": {
                    "panels": final_output["panels"],
                    "characters": final_output["characters"],
                    "debug": debug_data
                }
            }
        )

        return {
            "final_output": result["final_output"],
            "debug": {
                "scene_data": result.get("scene_data"),
                "character_data": result.get("character_data"),
                "dialogue_data": result.get("dialogue_data"),
            }
        }

    except Exception as exc:
        logger.error("Orchestrator generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))