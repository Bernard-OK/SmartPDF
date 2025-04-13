import re

def clean_text(text: str) -> str:
    """
    Clean raw blog text:
    - Remove multiple spaces
    - Strip leading/trailing whitespace
    - Remove script or style blocks if any
    - Normalize to readable form
    """
    # Remove HTML tags if any slipped through
    text = re.sub(r'<[^>]+>', '', text)

    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove weird characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    return text.strip()