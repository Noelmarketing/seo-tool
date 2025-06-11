import re
from collections import Counter
from typing import Dict


def extract_keywords(text: str, top_n: int = 20) -> Dict[str, int]:
    """Return top keywords and their frequencies."""
    words = re.findall(r"\b[\w-]+\b", text.lower())
    counts = Counter(words)
    return dict(counts.most_common(top_n))
