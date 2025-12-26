"""Prompt templates and system instructions."""
from .system import get_system_prompt, CRISIS_SYSTEM_PROMPT
from .templates import (
    EMPATHY_RESPONSES,
    GROUNDING_EXERCISES,
    CRISIS_RESOURCES,
    get_response_template,
)

__all__ = [
    "get_system_prompt",
    "CRISIS_SYSTEM_PROMPT",
    "EMPATHY_RESPONSES",
    "GROUNDING_EXERCISES", 
    "CRISIS_RESOURCES",
    "get_response_template",
]
