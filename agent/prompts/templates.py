"""
Response Templates for Cycology Agent.

Pre-crafted empathetic responses, grounding exercises, and crisis resources
that can be inserted or adapted in agent responses.
"""

from typing import Dict, List
from ..core.state import MoodType, CrisisLevel


# ============================================================================
# EMPATHY RESPONSE LIBRARY
# ============================================================================

EMPATHY_RESPONSES: Dict[str, List[str]] = {
    "validation": [
        "That sounds really difficult. I'm glad you're sharing this with me.",
        "What you're feeling makes complete sense given what you've been through.",
        "Your feelings are valid, and it's okay to feel this way.",
        "Thank you for trusting me with this. It takes courage to open up.",
        "I hear you, and I want you to know that what you're experiencing matters.",
    ],
    
    "acknowledgment": [
        "I can see this is weighing heavily on you.",
        "It sounds like you've been carrying a lot.",
        "That must be really exhausting to deal with.",
        "I'm sorry you're going through this.",
        "It's clear this situation is really affecting you.",
    ],
    
    "presence": [
        "I'm here with you, and I'm listening.",
        "Take your time. There's no rush.",
        "You don't have to go through this alone.",
        "I'm not going anywhere. I'm here.",
        "Whatever you need to share, I'm ready to hear it.",
    ],
    
    "hope": [
        "Even in dark moments, it's okay to hope for brighter days.",
        "You've gotten through difficult times before, and you're still here.",
        "Small steps forward are still steps forward.",
        "It's okay if today is just about getting through today.",
        "Things can change, even when it doesn't feel that way right now.",
    ],
    
    "encouragement": [
        "The fact that you're talking about this shows real strength.",
        "Reaching out is one of the bravest things you can do.",
        "You're doing the best you can, and that's enough.",
        "Be gentle with yourself. You're going through a lot.",
        "Taking care of your mental health is never something to be ashamed of.",
    ],
}


# ============================================================================
# GROUNDING EXERCISES
# ============================================================================

GROUNDING_EXERCISES: Dict[str, str] = {
    "5-4-3-2-1": """Here's a grounding technique that can help bring you back to the present:

**The 5-4-3-2-1 Method:**
- **5** things you can SEE around you
- **4** things you can TOUCH or feel
- **3** things you can HEAR right now
- **2** things you can SMELL
- **1** thing you can TASTE

Take your time with each one. This helps anchor you in the present moment.""",

    "breathing": """Let's try some calming breaths together:

**Box Breathing:**
1. Breathe IN slowly for 4 seconds
2. HOLD your breath for 4 seconds
3. Breathe OUT slowly for 4 seconds
4. HOLD empty for 4 seconds

Repeat this 3-4 times. There's no wrong way to do this.""",

    "body_scan": """Let's do a quick body scan to help you feel more grounded:

1. Start by feeling your feet on the ground
2. Notice the weight of your body in your seat
3. Feel your hands - are they tense or relaxed?
4. Relax your shoulders away from your ears
5. Unclench your jaw
6. Take a deep breath

How does that feel?""",

    "safe_place": """Let's create a mental safe space:

Close your eyes if comfortable. Imagine a place where you feel completely safe and at peace.

- What does it look like?
- What sounds are there?
- What does the air feel like?
- Are you alone or with others?

You can return to this place anytime you need it.""",

    "cold_water": """A quick physical grounding technique:

If you have access to cold water:
1. Splash some cold water on your face
2. Or hold ice cubes in your hands
3. Or run cold water over your wrists

The physical sensation can help interrupt overwhelming thoughts and bring you back to the present.""",
}


# ============================================================================
# CRISIS RESOURCES
# ============================================================================

CRISIS_RESOURCES: Dict[str, Dict[str, str]] = {
    "india": {
        "iCall": "9152987821 (Mon-Sat 8am-10pm)",
        "Vandrevala Foundation": "1860-2662-345 (24/7)",
        "NIMHANS": "080-46110007",
        "Snehi": "044-24640050 (24/7)",
        "AASRA": "91-22-27546669 (24/7)",
    },
    "us": {
        "988 Suicide & Crisis Lifeline": "988 (24/7)",
        "Crisis Text Line": "Text HOME to 741741",
        "SAMHSA Helpline": "1-800-662-4357",
    },
    "uk": {
        "Samaritans": "116 123 (24/7)",
        "CALM": "0800 58 58 58 (5pm-midnight)",
        "Shout": "Text SHOUT to 85258",
    },
    "international": {
        "International Association for Suicide Prevention": "https://www.iasp.info/resources/Crisis_Centres/",
        "Befrienders Worldwide": "https://www.befrienders.org/",
        "Find a Helpline": "https://findahelpline.com/",
    },
}


def format_crisis_resources(region: str = "india") -> str:
    """Format crisis resources for a specific region."""
    resources = CRISIS_RESOURCES.get(region, CRISIS_RESOURCES["international"])
    
    lines = [f"🆘 **Crisis Resources ({region.title()}):**"]
    for name, contact in resources.items():
        lines.append(f"- {name}: {contact}")
    
    # Always add international
    if region != "international":
        lines.append("\n🌍 **International Resources:**")
        for name, contact in CRISIS_RESOURCES["international"].items():
            lines.append(f"- {name}: {contact}")
    
    return "\n".join(lines)


# ============================================================================
# RESPONSE TEMPLATES BY SITUATION
# ============================================================================

RESPONSE_TEMPLATES: Dict[str, str] = {
    "greeting": """Hello! I'm Cycology, and I'm here to listen and support you. 

Whether you want to talk about what's on your mind, work through some feelings, or just have someone to chat with - I'm here. 

How are you feeling today?""",

    "crisis_immediate": """I'm really concerned about what you've shared, and I need you to know that you matter. What you're feeling right now is real and overwhelming, but please don't face this alone.

{crisis_resources}

Would you be willing to reach out to one of these helplines right now? They have trained counselors who can help in ways I can't. I'll still be here, but your safety comes first.""",

    "escalation_gentle": """I've noticed you're going through something really significant. While I'm here to support you, I think it might be helpful to talk to a professional who can offer more specialized help.

Would you be open to exploring some options for speaking with a counselor or therapist? I can help you think through what that might look like.""",

    "session_end": """Thank you for sharing with me today. Remember, it's okay to not have everything figured out.

A few reminders:
- You can come back and talk anytime
- Your feelings are valid, always
- Be gentle with yourself

Take care of yourself. 💙""",

    "unclear_input": """I want to make sure I understand you correctly. Could you tell me a bit more about what's on your mind?

I'm here to listen, whatever it is.""",
}


def get_response_template(
    template_name: str,
    **kwargs
) -> str:
    """
    Get and format a response template.
    
    Args:
        template_name: Name of the template to use
        **kwargs: Variables to format into the template
        
    Returns:
        Formatted response string
    """
    template = RESPONSE_TEMPLATES.get(template_name, "")
    
    if not template:
        return ""
    
    try:
        return template.format(**kwargs)
    except KeyError:
        return template
