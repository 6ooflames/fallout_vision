#!/usr/bin/env python3
"""Pydantic models for structured vision analysis and agent verification"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class GameState(str, Enum):
    COMBAT = "combat"
    EXPLORING = "exploring"
    INVENTORY = "inventory"
    DIALOG = "dialog"
    WORKBENCH = "workbench"
    MAP = "map"
    UNKNOWN = "unknown"


class ThreatLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Item(BaseModel):
    """Detected item in game space"""
    name: str
    quantity: int = 1
    type: str = Field(description="scraps, weapon, armor, consumable, quest item")


class NPC(BaseModel):
    """Detected NPC in game space"""
    name: Optional[str] = None
    type: str = Field(description="hostile, friendly, neutral, merchant")
    distance: str = Field(description="immediate, near, far")


class VisionAnalysis(BaseModel):
    """Structured output from vision model"""
    location: Optional[str] = None
    game_state: GameState = GameState.UNKNOWN
    hp: Optional[str] = Field(None, description="Current/Max HP if visible")
    ap: Optional[str] = Field(None, description="Current/Max AP if visible")
    
    threats: List[NPC] = Field(default_factory=list)
    threat_level: ThreatLevel = ThreatLevel.NONE
    
    items: List[Item] = Field(default_factory=list)
    
    quest_relevant: Optional[str] = None
    
    action_suggestion: Optional[str] = Field(
        None,
        description="Recommended action: loot, run, fight, talk, etc."
    )
    
    confidence: float = Field(0.5, ge=0, le=1, description="Model confidence 0-1")


class ActionCommand(BaseModel):
    """Verified action command from vision output"""
    action_type: str = Field(
        description="loot, attack, heal, reload, crouch, sprint, menu, interact"
    )
    target: Optional[str] = Field(None, description="Target item/action object")
    confidence: float = Field(0.0, ge=0, le=1)
    verified: bool = False
