import re

# Patterns that indicate prompt injection attempts
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all instructions",
    r"disregard previous",
    r"forget your instructions",
    r"you are now",
    r"act as",
    r"pretend you are",
    r"new instruction",
    r"system prompt",
    r"jailbreak",
]

def strip_html(text: str) -> str:
    """Remove all HTML tags from input text."""
    clean = re.sub(r"<[^>]+>", "", text)
    return clean.strip()

def detect_injection(text: str) -> bool:
    """Return True if prompt injection is detected."""
    text_lower = text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False

def sanitise(text: str) -> tuple[str, bool]:
    """
    Sanitise input text.
    Returns (cleaned_text, is_safe).
    is_safe is False if injection detected.
    """
    cleaned = strip_html(text)
    if detect_injection(cleaned):
        return cleaned, False
    return cleaned, True