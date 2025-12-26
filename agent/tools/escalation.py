"""
Escalation Logic for Cycology Agent.

Determines when a conversation should be escalated to professional
human support based on crisis levels and conversation patterns.
"""

from typing import Optional
from dataclasses import dataclass

from ..core.state import CrisisLevel, MoodType


@dataclass
class EscalationDecision:
    """Result of escalation check."""
    should_escalate: bool
    urgency: str  # "immediate", "soon", "suggested", "none"
    reason: Optional[str]
    recommended_action: str


class EscalationChecker:
    """
    Determines when professional escalation is appropriate.
    
    Factors considered:
    - Crisis level
    - Mood deterioration
    - Conversation duration
    - User's responsiveness
    """
    
    def check(
        self,
        crisis_level: CrisisLevel,
        current_mood: MoodType,
        mood_trend: str,
        conversation_turns: int,
        user_rejected_resources: bool = False,
    ) -> EscalationDecision:
        """
        Check if escalation to professional support is needed.
        
        Args:
            crisis_level: Current detected crisis level
            current_mood: Current mood assessment
            mood_trend: Mood trend ("improving", "stable", "declining")
            conversation_turns: Number of conversation turns
            user_rejected_resources: Whether user has rejected help before
            
        Returns:
            EscalationDecision with recommendation
        """
        
        # Critical crisis - immediate escalation
        if crisis_level == CrisisLevel.CRITICAL:
            return EscalationDecision(
                should_escalate=True,
                urgency="immediate",
                reason="User expressing immediate danger signals",
                recommended_action=(
                    "Provide crisis hotline numbers immediately. "
                    "Do not leave the conversation abruptly. "
                    "Encourage calling emergency services if in immediate danger."
                )
            )
        
        # High crisis - urgent escalation
        if crisis_level == CrisisLevel.HIGH:
            return EscalationDecision(
                should_escalate=True,
                urgency="soon",
                reason="User showing serious distress indicators",
                recommended_action=(
                    "Strongly recommend professional support. "
                    "Share crisis resources. "
                    "Validate their experience while encouraging help-seeking."
                )
            )
        
        # Medium crisis with declining mood - suggest escalation
        if crisis_level == CrisisLevel.MEDIUM and mood_trend == "declining":
            return EscalationDecision(
                should_escalate=True,
                urgency="suggested",
                reason="User's distress level increasing over conversation",
                recommended_action=(
                    "Gently suggest speaking with a professional. "
                    "Offer resources but don't push if user declines. "
                    "Continue providing supportive presence."
                )
            )
        
        # Long conversation with no improvement
        if conversation_turns > 20 and mood_trend != "improving":
            return EscalationDecision(
                should_escalate=True,
                urgency="suggested",
                reason="Extended conversation without mood improvement",
                recommended_action=(
                    "Acknowledge the conversation has been long. "
                    "Suggest that ongoing support from a professional might help. "
                    "Reassure that continuing to talk is also okay."
                )
            )
        
        # Severe negative moods without crisis
        severe_moods = {MoodType.OVERWHELMED, MoodType.LONELY}
        if current_mood in severe_moods and conversation_turns > 10:
            return EscalationDecision(
                should_escalate=False,  # Don't force, but mention
                urgency="suggested",
                reason="User experiencing significant emotional difficulty",
                recommended_action=(
                    "When natural, mention that professional support is available. "
                    "Don't make it the focus unless user shows interest."
                )
            )
        
        # No escalation needed
        return EscalationDecision(
            should_escalate=False,
            urgency="none",
            reason=None,
            recommended_action="Continue normal supportive conversation."
        )


# Singleton instance
_checker = EscalationChecker()


def should_escalate(
    crisis_level: CrisisLevel,
    current_mood: MoodType,
    mood_trend: str,
    conversation_turns: int,
    user_rejected_resources: bool = False,
) -> EscalationDecision:
    """
    Convenience function for escalation checking.
    
    Args:
        crisis_level: Current crisis level
        current_mood: Current mood
        mood_trend: Mood trend over conversation
        conversation_turns: Number of turns in conversation
        user_rejected_resources: Whether user has declined resources
        
    Returns:
        EscalationDecision result
    """
    return _checker.check(
        crisis_level=crisis_level,
        current_mood=current_mood,
        mood_trend=mood_trend,
        conversation_turns=conversation_turns,
        user_rejected_resources=user_rejected_resources,
    )
