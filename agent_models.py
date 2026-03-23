#!/usr/bin/env python3
"""Pydantic models for agent call verification"""

from pydantic import BaseModel, Field, ValidationError
from enum import Enum
import json


class ActionType(str, Enum):
    HEAL = "HEAL"
    VATS = "VATS"
    NONE = "NONE"


class VisionAction(BaseModel):
    """Structured agent action with strict validation"""
    action: ActionType = Field(..., description="The action to take in the game")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0.0 to 1.0")
    reasoning: str = Field(..., description="Why this action was chosen")


def validate_llm_response(raw_text: str) -> VisionAction:
    """Extracts and validates JSON from the LLM, returning a Pydantic model"""
    try:
        # Strip markdown if the LLM wrapped it
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
            
        data = json.loads(cleaned)
        return VisionAction(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        # Fallback to NONE on failure to prevent rogue keyboard inputs
        return VisionAction(
            action=ActionType.NONE,
            confidence=0.0,
            reasoning=f"Validation failed: {str(e)}"
        )
