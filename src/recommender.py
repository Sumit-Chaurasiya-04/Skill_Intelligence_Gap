import json
import os
import random
from . import utils # Use relative import

# Load the full skill list and a simple map of related skills
SKILL_LIST = utils.load_skills()

# Pre-defined mapping for intelligent (non-random) recommendations
# This simulates a knowledge graph or LLM reasoning
SKILL_RELATIONS = {
    "Python": ["SQL", "Git", "Docker", "Data Analysis"],
    "SQL": ["Data Analysis", "Python", "Excel", "Power BI"],
    "Machine Learning": ["Python", "TensorFlow", "Statistics", "Deep Learning"],
    "Deep Learning": ["PyTorch", "TensorFlow", "Machine Learning", "AWS"],
    "Data Analysis": ["SQL", "Excel", "Data Visualization", "Communication"],
    "Natural Language Processing": ["Python", "Machine Learning", "PyTorch", "Communication"],
    "TensorFlow": ["Deep Learning", "Python", "AWS", "Git"],
    "PyTorch": ["Deep Learning", "Machine Learning", "Python", "AWS"],
    "Data Visualization": ["Tableau", "Power BI", "Excel", "Data Analysis"],
    "AWS": ["Docker", "Linux", "Git", "Python"],
    "Communication": ["Problem Solving", "Data Analysis"],
    "Problem Solving": ["Communication", "Git", "Linux"],
}

def recommend_skills(skill: str, top_n: int = 5):
    """
    Recommend related skills using a pre-defined knowledge graph and filling with popular skills.
    Avoids purely random choices.
    """
    skill_key = skill
    # Find the best match in the keys (case-insensitive)
    for k in SKILL_RELATIONS.keys():
        if skill.lower() == k.lower():
            skill_key = k
            break
        
    related = []
    # 1. Get explicit relations from the map
    if skill_key in SKILL_RELATIONS:
        related.extend(SKILL_RELATIONS[skill_key])

    # 2. Fill up with popular/general skills if needed
    popular_skills = [s for s in SKILL_LIST if s not in related and s.lower() != skill_key.lower()]
    random.shuffle(popular_skills)

    # Combine and ensure uniqueness and exclusion of the input skill
    final_recs = list(set([s for s in related + popular_skills if s.lower() != skill_key.lower()]))

    return final_recs[:top_n]
