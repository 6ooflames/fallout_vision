#!/usr/bin/env python3
"""Pytest suite for agent models validation"""

import pytest
from agent_models import VisionAction, ActionType, validate_llm_response


def test_valid_heal():
    """Test valid HEAL action"""
    output = '{"action": "HEAL", "confidence": 0.95, "reasoning": "Low HP"}'
    result = validate_llm_response(output)
    assert result.action == ActionType.HEAL
    assert result.confidence == 0.95


def test_valid_vats():
    """Test valid VATS action with markdown"""
    output = "```json\n{\"action\": \"VATS\", \"confidence\": 0.8, \"reasoning\": \"Enemy seen\"}\n```"
    result = validate_llm_response(output)
    assert result.action == ActionType.VATS
    assert result.confidence == 0.8


def test_invalid_action_fallback():
    """Test invalid action type falls back to NONE"""
    output = '{"action": "JUMP", "confidence": 0.9, "reasoning": "Obstacle"}'
    result = validate_llm_response(output)
    assert result.action == ActionType.NONE
    assert "Validation failed" in result.reasoning


def test_missing_fields_fallback():
    """Test missing required fields falls back to NONE"""
    output = '{"action": "HEAL"}'
    result = validate_llm_response(output)
    assert result.action == ActionType.NONE
    assert "Validation failed" in result.reasoning


def test_low_confidence_still_valid():
    """Test that low confidence is still accepted if valid"""
    output = '{"action": "HEAL", "confidence": 0.15, "reasoning": "Uncertain but try to heal"}'
    result = validate_llm_response(output)
    assert result.action == ActionType.HEAL
    assert result.confidence == 0.15


def test_high_confidence_still_valid():
    """Test that high confidence is accepted"""
    output = '{"action": "VATS", "confidence": 0.99, "reasoning": "Very confident enemy visible"}'
    result = validate_llm_response(output)
    assert result.action == ActionType.VATS
    assert result.confidence == 0.99
