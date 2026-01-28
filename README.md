Skill Gap Intelligence Engine (FOSS)

A professional, Python-based application for data-driven career planning. This engine identifies skill gaps, analyzes job market dynamics, and provides actionable, personalized recommendations using only Free and Open-Source Software (FOSS) tools.

Core Functionality

This application showcases a full-stack, data-driven system built on lightweight, performant modules.


Project Architecture

The project follows a modular, package-based Python structure to ensure separation of concerns (SoC), portability, and testability.

Key Components

app/main_app.py: The application entry point. Handles all Streamlit UI components, session state, and orchestration of logic calls from the src/ package.

src/: The core Python package containing all business logic, algorithms, and data handlers. This clean separation makes the code platform-agnostic.

data/: Storage for structured data (skill_taxonomy.json) and the persistent database (skills.db).

Development Philosophy

The entire stack is built to be lightweight and scalable, adhering to the FOSS constraint while demonstrating high-level concepts like:

Modular Programming: Use of the src package (__init__.py) and relative imports.

Dependency Management: Strict use of a single requirements.txt.

Error Handling: Robust path resolution (src/utils.py) and database connection management (src/database.py).

Local Setup and Deployment

Prerequisites

Python 3.13 (or 3.10+ for wider compatibility)

pip (Python package installer)

1. Installation

Clone the Repository:

git clone [https://github.com/Sumit-Chaurasiya-04/Skill_Intelligence_Gap.git](https://github.com/Sumit-Chaurasiya-04/Skill_Intelligence_Gap.git)
cd Skill_Intelligence_Gap


Create and Activate Virtual Environment (Recommended):

python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate.bat # Windows Command Prompt


Install Dependencies:

pip install -r requirements.txt


2. Run Locally

Execute the main Streamlit application file:

streamlit run app/main_app.py


3. Deploy to Streamlit Cloud

The application is configured for one-click deployment:

Log in to Streamlit Community Cloud with GitHub.

Select the repository: Sumit-Chaurasiya-04/Skill_Intelligence_Gap.

Set the Main file path to: app/main_app.py.

Click Deploy!

Contributing

This project is licensed under the MIT License. Contributions, suggestions, and bug reports are welcome! Please open an issue or submit a pull request for any improvements, especially to the recommendation logic or data pipeline simulation.

Author: Sumit Chaurasiya
