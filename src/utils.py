import json
import os
import pandas as pd
import sys

# Define base paths relative to the project root
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)
JOBS_FILE = os.path.join(DATA_DIR, "jobs_db.json")
SKILL_TAXONOMY_FILE = os.path.join(DATA_DIR, "skill_taxonomy.json")

def initialize_data_files():
    """
    Ensures the skill taxonomy file exists with a robust default list.
    Called on application startup.
    """
    if not os.path.exists(SKILL_TAXONOMY_FILE):
        print("Initializing default skill taxonomy.")
        default_skills = [
            "Python", "SQL", "Machine Learning", "Deep Learning", "Data Analysis",
            "Natural Language Processing", "TensorFlow", "PyTorch", "Tableau",
            "Power BI", "Data Visualization", "AWS", "Azure", "Git", "Docker",
            "Linux", "Communication", "Problem Solving", "Java", "JavaScript", "React"
        ]
        with open(SKILL_TAXONOMY_FILE, "w", encoding="utf-8") as f:
            json.dump(default_skills, f, indent=4)
        return default_skills
    return load_skills()

def load_skills():
    """Load skills from the taxonomy file."""
    if os.path.exists(SKILL_TAXONOMY_FILE):
        try:
            with open(SKILL_TAXONOMY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading skill taxonomy: {e}. Returning empty list.")
            return []
    return []

def save_jobs(df: pd.DataFrame):
    """Save jobs dataframe to JSON file for persistence."""
    if df.empty:
        # Save an empty list if no jobs were found to prevent file errors
        with open(JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return

    jobs_list = df.to_dict(orient="records")
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs_list, f, ensure_ascii=False, indent=2)

def load_jobs():
    """Load jobs from JSON file into a pandas DataFrame."""
    if not os.path.exists(JOBS_FILE):
        return pd.DataFrame()
    
    try:
        with open(JOBS_FILE, "r", encoding="utf-8") as f:
            jobs_list = json.load(f)
        return pd.DataFrame(jobs_list)
    except (json.JSONDecodeError, FileNotFoundError):
        return pd.DataFrame()

# Remove the deprecated modules and move the simple summarization to nlp_processing.py
# The initial version had an empty free_llm.py which is now integrated into nlp_processing.py
