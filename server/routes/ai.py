from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import os
from groq import Groq

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SuggestRequest(BaseModel):
    type: str   # storyline / tagline / summary
    context: str
    characters: Optional[List[str]] = [] 

def format_characters(chars):
    if not chars:
        return "No characters provided"
    
    text="" 
    for c in chars:
        if isinstance(c, str):
            text += f"\nName: {c}\n"
        else:
            text += f"""
            Name: {c.get('name')}
            Personality: {c.get('personality')}
            Style: {c.get('style')}
            Appearance: {c.get('appearance')}
            """
    return text



@router.post("/ai/suggest")
def suggest(data: SuggestRequest):
    
    char_context = format_characters(data.characters)

    prompt = f"""
    Generate a {data.type} for a comic story.
    Characters: {char_context}
    Context: {data.context}
    Keep it engaging and creative.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "suggestion": response.choices[0].message.content
    }