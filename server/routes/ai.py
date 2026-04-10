from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from groq import Groq
from orchestrator.logger import get_logger

router = APIRouter()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None
logger = get_logger("routes.ai")

class SuggestRequest(BaseModel):
    type: str   # storyline / tagline / summary
    context: str
    characters: Optional[List[str]] = [] 

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
    if client is None:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured on the server.")
    
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
