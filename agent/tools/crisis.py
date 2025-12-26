"""
Crisis Detection System for Cycology Agent.

Multi-layer crisis detection using keyword matching, pattern recognition,
and contextual analysis to identify users who may be at risk.
"""

import re
from typing import Tuple, List, Set
from dataclasses import dataclass

from ..core.state import CrisisLevel


@dataclass
class CrisisAssessment:
    """Result of crisis detection analysis."""
    level: CrisisLevel
    keywords_found: List[str]
    confidence: float  # 0.0 to 1.0
    requires_immediate_response: bool
    suggested_response_type: str  # "normal", "supportive", "resources", "crisis"


class CrisisDetector:
    """
    Multi-layer crisis detection system.
    
    Detection Layers:
    1. Critical keywords (immediate triggers)
    2. High-concern phrases
    3. Distress indicators
    4. Contextual patterns
    """
    
    # CRITICAL: Immediate intervention required
    CRITICAL_KEYWORDS: Set[str] = {
        # Suicide-related
        "kill myself", "end my life", "suicide", "suicidal",
        "want to die", "better off dead", "no reason to live",
        "ending it all", "take my own life", "don't want to be here",
        "can't go on", "goodbye forever", "final goodbye",
        
        # Self-harm
        "cut myself", "hurt myself", "self harm", "self-harm",
        "harming myself", "cutting", "burning myself",
        
        # Immediate danger
        "have a plan", "have pills", "have a gun", "have a knife",
        "going to do it", "tonight is the night", "this is my last",
    }
    
    # HIGH: Serious concern, strong intervention needed
    HIGH_CONCERN_PHRASES: Set[str] = {
        # Hopelessness
        "no hope", "hopeless", "nothing matters", "pointless",
        "no way out", "trapped", "can't escape", "no future",
        "never get better", "always be like this",
        
        # Extreme distress
        "can't take it anymore", "at my breaking point", "falling apart",
        "losing my mind", "going crazy", "can't handle this",
        "unbearable", "too much pain",
        
        # Isolation
        "nobody cares", "no one would notice", "better without me",
        "burden to everyone", "all alone", "completely alone",
        
        # Past attempts
        "tried before", "attempted before", "last time i tried",
    }
    
    # MEDIUM: Significant distress, offer resources
    MEDIUM_CONCERN_PHRASES: Set[str] = {
        # Depression indicators
        "so depressed", "deeply depressed", "severe depression",
        "can't get out of bed", "can't function", "empty inside",
        "numb", "don't feel anything", "stopped caring",
        
        # Anxiety/Panic
        "panic attack", "severe anxiety", "can't breathe",
        "chest is tight", "going to pass out", "losing control",
        
        # Relationship crisis
        "everyone left me", "relationship ended", "divorce",
        "lost custody", "lost my job", "lost everything",
        
        # Trauma
        "flashback", "nightmare", "can't stop thinking about",
        "haunted by", "trauma", "abused",
    }
    
    # LOW: Monitor and be attentive
    LOW_CONCERN_PHRASES: Set[str] = {
        # General distress
        "feeling down", "sad lately", "stressed out",
        "overwhelmed", "anxious", "worried",
        "can't sleep", "not eating", "exhausted",
        "lonely", "isolated", "struggling",
    }
    
    def __init__(self):
        """Initialize the crisis detector."""
        # Compile patterns for efficient matching
        self._critical_pattern = self._compile_pattern(self.CRITICAL_KEYWORDS)
        self._high_pattern = self._compile_pattern(self.HIGH_CONCERN_PHRASES)
        self._medium_pattern = self._compile_pattern(self.MEDIUM_CONCERN_PHRASES)
        self._low_pattern = self._compile_pattern(self.LOW_CONCERN_PHRASES)
    
    def _compile_pattern(self, phrases: Set[str]) -> re.Pattern:
        """Compile a set of phrases into a regex pattern."""
        escaped = [re.escape(phrase) for phrase in phrases]
        return re.compile(r'\b(' + '|'.join(escaped) + r')\b', re.IGNORECASE)
    
    def _find_matches(self, text: str, pattern: re.Pattern) -> List[str]:
        """Find all matches of a pattern in text."""
        return [match.group(0).lower() for match in pattern.finditer(text)]
    
    def detect(self, message: str, conversation_history: List[str] = None) -> CrisisAssessment:
        """
        Analyze a message for crisis indicators.
        
        Args:
            message: The user's message to analyze
            conversation_history: Previous messages for context (optional)
            
        Returns:
            CrisisAssessment with detected level and details
        """
        text = message.lower()
        keywords_found = []
        
        # Layer 1: Check critical keywords (highest priority)
        critical_matches = self._find_matches(text, self._critical_pattern)
        if critical_matches:
            keywords_found.extend(critical_matches)
            return CrisisAssessment(
                level=CrisisLevel.CRITICAL,
                keywords_found=keywords_found,
                confidence=0.95,
                requires_immediate_response=True,
                suggested_response_type="crisis"
            )
        
        # Layer 2: Check high concern phrases
        high_matches = self._find_matches(text, self._high_pattern)
        if high_matches:
            keywords_found.extend(high_matches)
            return CrisisAssessment(
                level=CrisisLevel.HIGH,
                keywords_found=keywords_found,
                confidence=0.85,
                requires_immediate_response=True,
                suggested_response_type="crisis"
            )
        
        # Layer 3: Check medium concern phrases
        medium_matches = self._find_matches(text, self._medium_pattern)
        if medium_matches:
            keywords_found.extend(medium_matches)
            return CrisisAssessment(
                level=CrisisLevel.MEDIUM,
                keywords_found=keywords_found,
                confidence=0.70,
                requires_immediate_response=False,
                suggested_response_type="resources"
            )
        
        # Layer 4: Check low concern phrases
        low_matches = self._find_matches(text, self._low_pattern)
        if low_matches:
            keywords_found.extend(low_matches)
            return CrisisAssessment(
                level=CrisisLevel.LOW,
                keywords_found=keywords_found,
                confidence=0.50,
                requires_immediate_response=False,
                suggested_response_type="supportive"
            )
        
        # No concerning indicators found
        return CrisisAssessment(
            level=CrisisLevel.NONE,
            keywords_found=[],
            confidence=0.90,
            requires_immediate_response=False,
            suggested_response_type="normal"
        )
    
    def get_escalation_urgency(self, level: CrisisLevel) -> str:
        """Get urgency description for a crisis level."""
        urgency_map = {
            CrisisLevel.CRITICAL: "IMMEDIATE - Potential imminent danger",
            CrisisLevel.HIGH: "URGENT - Serious distress, intervention needed",
            CrisisLevel.MEDIUM: "ELEVATED - Significant distress, offer resources",
            CrisisLevel.LOW: "MONITOR - Mild distress, be attentive",
            CrisisLevel.NONE: "NORMAL - No immediate concerns",
        }
        return urgency_map.get(level, "UNKNOWN")


# Singleton instance
_detector = CrisisDetector()


def detect_crisis(message: str, conversation_history: List[str] = None) -> CrisisAssessment:
    """
    Convenience function for crisis detection.
    
    Args:
        message: Message to analyze
        conversation_history: Optional conversation context
        
    Returns:
        CrisisAssessment result
    """
    return _detector.detect(message, conversation_history)
