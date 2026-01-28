import re
from rapidfuzz import fuzz
from collections import Counter
import json
import os
from . import utils # Use relative import

# Load the skills taxonomy (now handled via utils)
SKILL_LIST = utils.load_skills()
SKILL_TO_TOKENS = {skill.lower(): skill for skill in SKILL_LIST}
ACRONYMS = {"ml": "Machine Learning", "dl": "Deep Learning", "ai": "Artificial Intelligence", "nlp": "Natural Language Processing", "db": "Database"}


def extract_skills(text: str, threshold: int = 85):
    """
    Extract skills from text using robust, tokenized fuzzy matching against the taxonomy.
    This avoids heavy external libraries and works reliably.
    """
    if not text or not SKILL_LIST:
        return []

    text_lower = text.lower()
    found_skills = set()

    # 1. Exact Phrase and Acronym Matching (Most reliable)
    for token_lower, full_skill in SKILL_TO_TOKENS.items():
        if token_lower in text_lower:
            found_skills.add(full_skill)

    for acro, full_skill in ACRONYMS.items():
        # Check for acronyms surrounded by spaces or punctuation
        if re.search(r'\b' + re.escape(acro) + r'\b', text_lower):
            found_skills.add(full_skill)

    # 2. Tokenized Fuzzy Matching (for variations/typos)
    # Tokenize text into words/phrases up to 3 words long
    words = re.findall(r'\b\w+\b', text_lower)
    tokens = words + [words[i] + ' ' + words[i+1] for i in range(len(words)-1)] + \
             [words[i] + ' ' + words[i+1] + ' ' + words[i+2] for i in range(len(words)-2)]

    for skill in SKILL_LIST:
        skill_lower = skill.lower()
        if skill not in found_skills:
            # Check against text tokens using rapidfuzz for close matches
            if any(fuzz.ratio(skill_lower, token) >= threshold for token in tokens):
                found_skills.add(skill)

    return sorted(list(found_skills))

def summarize_text(text: str, max_length: int = 180):
    """
    Lightweight summarization and keyword extraction (as an LLM replacement).
    """
    if not text:
        return ""

    # Simple sentence-based summarization
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    summary = " ".join(sentences[:3])
    summary = (summary[:max_length].rsplit(' ', 1)[0] + "...") if len(summary) > max_length else summary

    # Keyword extraction
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    # A slightly more comprehensive stop word list
    stop = {"the", "and", "with", "from", "that", "this", "have", "will", "your", "their", "our", "for", "are", "was", "but", "not", "has"}
    words = [w for w in words if w not in stop]
    
    # Use CountVectorizer style for more robust weighting (simulated with Counter)
    keywords = [w for w, _ in Counter(words).most_common(5)]
    
    summary += f"\n\nKey Terms: {', '.join(keywords)}"
    return summary
