"""
Mood Analysis System for Cycology Agent.

Analyzes user messages to detect emotional state and track mood changes
over the conversation.
"""

import re
from typing import Tuple, List, Dict
from dataclasses import dataclass

from ..core.state import MoodType


@dataclass
class MoodAssessment:
    """Result of mood analysis."""
    mood: MoodType
    confidence: float  # 0.0 to 1.0
    score: float       # -1.0 (very negative) to 1.0 (very positive)
    indicators: List[str]


class MoodAnalyzer:
    """
    Sentiment and mood detection system.
    
    Uses keyword matching and pattern analysis to determine
    the emotional state of user messages.
    """
    
    # Mood indicator keywords with weights
    MOOD_INDICATORS: Dict[MoodType, Dict[str, float]] = {
        MoodType.HAPPY: {
            "happy": 0.8, "joy": 0.9, "excited": 0.8, "great": 0.7,
            "amazing": 0.9, "wonderful": 0.8, "fantastic": 0.9,
            "love": 0.6, "grateful": 0.7, "blessed": 0.7,
            "thrilled": 0.9, "delighted": 0.8, "ecstatic": 0.95,
            "elated": 0.9, "cheerful": 0.7, "joyful": 0.85,
            ":)": 0.5, "😊": 0.6, "😄": 0.7, "❤️": 0.5,
        },
        
        MoodType.CONTENT: {
            "content": 0.8, "peaceful": 0.8, "calm": 0.7, "relaxed": 0.7,
            "okay": 0.5, "fine": 0.5, "good": 0.6, "nice": 0.6,
            "comfortable": 0.7, "satisfied": 0.7, "serene": 0.8,
            "tranquil": 0.8, "at ease": 0.7, "settled": 0.6,
        },
        
        MoodType.SAD: {
            "sad": 0.8, "depressed": 0.9, "down": 0.6, "unhappy": 0.8,
            "miserable": 0.9, "heartbroken": 0.9, "grief": 0.9,
            "crying": 0.7, "tears": 0.6, "loss": 0.6, "mourning": 0.8,
            "devastated": 0.95, "despair": 0.9, "hopeless": 0.9,
            "empty": 0.8, "numb": 0.7, "broken": 0.8,
            "😢": 0.7, "😭": 0.8, "💔": 0.7,
        },
        
        MoodType.ANXIOUS: {
            "anxious": 0.9, "worried": 0.8, "nervous": 0.8, "scared": 0.8,
            "afraid": 0.8, "panic": 0.9, "terrified": 0.95, "fear": 0.8,
            "dread": 0.85, "uneasy": 0.7, "tense": 0.7, "stressed": 0.75,
            "overwhelmed": 0.8, "racing thoughts": 0.8, "can't breathe": 0.9,
            "heart pounding": 0.8, "shaking": 0.7, "trembling": 0.7,
        },
        
        MoodType.ANGRY: {
            "angry": 0.9, "furious": 0.95, "rage": 0.95, "mad": 0.8,
            "frustrated": 0.7, "annoyed": 0.6, "irritated": 0.6,
            "pissed": 0.8, "hate": 0.8, "resent": 0.75, "bitter": 0.7,
            "livid": 0.95, "outraged": 0.9, "infuriated": 0.9,
            "fed up": 0.7, "sick of": 0.7,
        },
        
        MoodType.CONFUSED: {
            "confused": 0.9, "lost": 0.7, "uncertain": 0.7, "unsure": 0.7,
            "don't know": 0.6, "not sure": 0.6, "mixed feelings": 0.7,
            "conflicted": 0.8, "torn": 0.7, "puzzled": 0.7,
            "bewildered": 0.8, "perplexed": 0.8, "unclear": 0.6,
        },
        
        MoodType.HOPEFUL: {
            "hopeful": 0.9, "optimistic": 0.85, "looking forward": 0.7,
            "excited about": 0.7, "can't wait": 0.7, "better": 0.6,
            "improving": 0.7, "progress": 0.6, "positive": 0.7,
            "encouraged": 0.8, "believing": 0.7, "faith": 0.6,
        },
        
        MoodType.OVERWHELMED: {
            "overwhelmed": 0.9, "too much": 0.8, "can't cope": 0.85,
            "drowning": 0.85, "swamped": 0.7, "buried": 0.7,
            "exhausted": 0.75, "burnt out": 0.85, "burnout": 0.85,
            "can't handle": 0.8, "falling apart": 0.85, "breaking down": 0.85,
        },
        
        MoodType.LONELY: {
            "lonely": 0.9, "alone": 0.7, "isolated": 0.85, "no friends": 0.85,
            "no one": 0.7, "by myself": 0.6, "abandoned": 0.9,
            "rejected": 0.8, "left out": 0.75, "excluded": 0.75,
            "disconnected": 0.8, "invisible": 0.8,
        },
    }
    
    # Score modifiers based on mood type
    MOOD_SCORES: Dict[MoodType, float] = {
        MoodType.HAPPY: 0.9,
        MoodType.CONTENT: 0.5,
        MoodType.NEUTRAL: 0.0,
        MoodType.HOPEFUL: 0.6,
        MoodType.CONFUSED: -0.1,
        MoodType.SAD: -0.7,
        MoodType.ANXIOUS: -0.5,
        MoodType.ANGRY: -0.4,
        MoodType.OVERWHELMED: -0.6,
        MoodType.LONELY: -0.6,
    }
    
    def __init__(self):
        """Initialize the mood analyzer."""
        pass
    
    def analyze(self, message: str) -> MoodAssessment:
        """
        Analyze a message for mood indicators.
        
        Args:
            message: The user's message to analyze
            
        Returns:
            MoodAssessment with detected mood and details
        """
        text = message.lower()
        
        # Find indicators for each mood
        mood_scores: Dict[MoodType, Tuple[float, List[str]]] = {}
        
        for mood, indicators in self.MOOD_INDICATORS.items():
            total_weight = 0.0
            found_indicators = []
            
            for keyword, weight in indicators.items():
                if keyword in text:
                    total_weight += weight
                    found_indicators.append(keyword)
            
            if found_indicators:
                mood_scores[mood] = (total_weight, found_indicators)
        
        # Determine the dominant mood
        if not mood_scores:
            return MoodAssessment(
                mood=MoodType.NEUTRAL,
                confidence=0.5,
                score=0.0,
                indicators=[]
            )
        
        # Find the mood with highest score
        best_mood = max(mood_scores.keys(), key=lambda m: mood_scores[m][0])
        weight, indicators = mood_scores[best_mood]
        
        # Calculate confidence based on weight and number of indicators
        confidence = min(0.95, 0.5 + (weight * 0.1) + (len(indicators) * 0.05))
        
        # Get the mood score
        score = self.MOOD_SCORES.get(best_mood, 0.0)
        
        return MoodAssessment(
            mood=best_mood,
            confidence=confidence,
            score=score,
            indicators=indicators
        )
    
    def get_mood_trend(
        self, 
        current_score: float, 
        previous_scores: List[float]
    ) -> str:
        """
        Determine mood trend based on recent scores.
        
        Args:
            current_score: Current mood score
            previous_scores: List of previous mood scores
            
        Returns:
            Trend: "improving", "declining", or "stable"
        """
        if not previous_scores:
            return "stable"
        
        avg_previous = sum(previous_scores) / len(previous_scores)
        diff = current_score - avg_previous
        
        if diff > 0.15:
            return "improving"
        elif diff < -0.15:
            return "declining"
        else:
            return "stable"


# Singleton instance
_analyzer = MoodAnalyzer()


def analyze_mood(message: str) -> MoodAssessment:
    """
    Convenience function for mood analysis.
    
    Args:
        message: Message to analyze
        
    Returns:
        MoodAssessment result
    """
    return _analyzer.analyze(message)
