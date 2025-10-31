import sqlite3
import os
import json
from datetime import datetime
import pandas as pd

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skills.db")

def init_db():
    """Initializes the SQLite database and creates the history table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                input_text TEXT,
                extracted_skills TEXT,
                recommendations TEXT
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def save_analysis(text: str, skills: list, recs: list):
    """Saves a user's skill analysis results to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO history(timestamp, input_text, extracted_skills, recommendations) VALUES (?,?,?,?)",
                    (datetime.now().isoformat(), text, json.dumps(skills), json.dumps(recs)))
        conn.commit()
    except Exception as e:
        print(f"Error saving analysis to database: {e}")
    finally:
        if conn:
            conn.close()

def load_history():
    """Loads all analysis history into a pandas DataFrame."""
    conn = None
    df = pd.DataFrame()
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
        # Convert JSON strings back to lists for display
        df['extracted_skills'] = df['extracted_skills'].apply(json.loads)
        df['recommendations'] = df['recommendations'].apply(json.loads)
    except pd.io.sql.DatabaseError:
        # This handles cases where the table hasn't been created yet
        df = pd.DataFrame(columns=['id', 'timestamp', 'input_text', 'extracted_skills', 'recommendations'])
    except Exception as e:
        print(f"Error loading history: {e}")
    finally:
        if conn:
            conn.close()
    return df
import sqlite3
import os
import json
from datetime import datetime
import pandas as pd

# Define the database path
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skills.db")

def init_db():
    """Initializes the SQLite database and creates the history table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                input_text TEXT,
                extracted_skills TEXT,
                recommendations TEXT
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn:
            conn.close()

def save_analysis(text: str, skills: list, recs: list):
    """Saves a user's skill analysis results to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO history(timestamp, input_text, extracted_skills, recommendations) VALUES (?,?,?,?)",
                    (datetime.now().isoformat(), text, json.dumps(skills), json.dumps(recs)))
        conn.commit()
    except Exception as e:
        print(f"Error saving analysis to database: {e}")
    finally:
        if conn:
            conn.close()

def load_history():
    """Loads all analysis history into a pandas DataFrame."""
    conn = None
    df = pd.DataFrame()
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
        # Convert JSON strings back to lists for display
        df['extracted_skills'] = df['extracted_skills'].apply(json.loads)
        df['recommendations'] = df['recommendations'].apply(json.loads)
    except pd.io.sql.DatabaseError:
        # This handles cases where the table hasn't been created yet
        df = pd.DataFrame(columns=['id', 'timestamp', 'input_text', 'extracted_skills', 'recommendations'])
    except Exception as e:
        print(f"Error loading history: {e}")
    finally:
        if conn:
            conn.close()
    return df
