import sys
import os
import json
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Setup and Imports
# -------------------------------
# Initialize Python path for importing 'src' directory
# This step is often necessary when running Streamlit from an unconventional directory
# Though __init__.py helps, this ensures robustness in VS Code execution.
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(PROJECT_ROOT)

try:
    # Relative imports from the 'src' package
    from src import nlp_processing, recommender, forecasting, data_pipeline, database, utils
except ImportError as e:
    st.error(f"Failed to import source modules. Ensure 'src' directory contains __init__.py. Error: {e}")
    st.stop()

# Initialize data and database structure
utils.initialize_data_files()
database.init_db()

# -------------------------------
# Session State Management
# -------------------------------
if 'analysis_ran' not in st.session_state:
    st.session_state.analysis_ran = False
if 'last_text' not in st.session_state:
    st.session_state.last_text = ""

# -------------------------------
# App UI Configuration
# -------------------------------
st.set_page_config(page_title="Skill Gap Intelligence Engine", layout="wide", initial_sidebar_state="expanded")
st.title("Skill Gap Intelligence Engine (Pro Bono)")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Skill Analysis", "Job Trend Tracker", "Analysis History"])

# -------------------------------
# PAGE: Skill Analysis
# -------------------------------
if page == "Skill Analysis":
    st.header("Analyze Your Profile")

    with st.expander("Paste Profile or Document Text Here"):
        input_text = st.text_area(
            "Copy & Paste Resume, Job Description, or Learning Goals:",
            value=st.session_state.last_text,
            height=300,
            key="input_text_area"
        )
        analyze_button = st.button("Analyze Profile (Powered by 2.5 Pro Bono)", use_container_width=True, type="primary")

    if analyze_button or st.session_state.analysis_ran:
        
        # Ensure we run analysis only on button click or if state dictates
        if analyze_button:
            st.session_state.analysis_ran = True
            st.session_state.last_text = input_text

        if not st.session_state.last_text.strip():
            st.warning("Please enter some text to analyze.")
            st.session_state.analysis_ran = False
        else:
            # Create a spinner for a better UX experience
            with st.spinner('Thinking deeply about your profile...'):
                text = st.session_state.last_text
                
                # 1. Extract skills
                extracted_skills = nlp_processing.extract_skills(text)
                
                # 2. Recommend related skills
                recommendations = []
                for skill in extracted_skills:
                    recommendations.extend(recommender.recommend_skills(skill))
                
                # Final unique recommendations
                unique_recs = sorted(list(set(recommendations) - set(extracted_skills)))
                
                # 3. Save the results to the database (New Feature!)
                database.save_analysis(text, extracted_skills, unique_recs)

            st.subheader("Analysis Results:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Extracted Core Skills (Your Assets)")
                if extracted_skills:
                    st.success(f"{len(extracted_skills)} Skills Identified.")
                    st.markdown(f"**{', '.join(extracted_skills)}**")
                else:
                    st.info("No recognizable skills detected against the taxonomy.")
                    
            with col2:
                st.markdown("##### Recommended Skill Gaps (Next Steps)")
                if unique_recs:
                    st.warning(f"{len(unique_recs)} Growth Areas Suggested.")
                    st.markdown(f"**{', '.join(unique_recs)}**")
                else:
                    st.success("You seem to have a comprehensive skill set!")

            # 4. Summarize Text (LLM Simulation)
            st.markdown("---")
            st.subheader("Text Overview (Simulated LLM Summary)")
            summary = nlp_processing.summarize_text(text)
            st.code(summary, language='text')

# -------------------------------
# PAGE: Job Trend Tracker
# -------------------------------
elif page == "Job Trend Tracker":
    st.header("Job Market Trend & Scraper")

    # ----- Job Scraper -----
    st.subheader("Live Job Scraper (Simulated)")
    col_k, col_p = st.columns([3, 1])
    with col_k:
        keyword = st.text_input("Enter Job Role Keyword:", "Data Scientist", key="job_keyword")
    with col_p:
        pages = st.number_input("Pages to Scrape (Max 5)", min_value=1, max_value=5, value=1, key="job_pages")
    
    if st.button("Fetch & Analyze Jobs", use_container_width=True, type="primary"):
        # Run the updated, safer scraping function
        with st.spinner(f"Simulating scrape for '{keyword}' over {pages} pages..."):
            jobs_df = data_pipeline.scrape_jobs(keyword, pages)
            
        if jobs_df.empty:
            st.error("No jobs found or simulated fetch failed. Try a different keyword.")
        else:
            st.success(f"Successfully fetched and analyzed {len(jobs_df)} simulated job postings.")
            
    # ----- Previously Scraped Jobs -----
    st.markdown("---")
    st.subheader("Previously Fetched Jobs Data")
    
    prev_jobs = utils.load_jobs()
    if not prev_jobs.empty:
        st.dataframe(prev_jobs, use_container_width=True)

        # ----- Trend Forecasting -----
        st.subheader("Simulated Skill Demand Trend")
        
        # Use one of the most common skills from the scraped jobs, or default
        all_descriptions = ' '.join(prev_jobs['description'].fillna(''))
        # Use nlp_processing to find a skill in the scraped data descriptions
        scraped_skills = nlp_processing.extract_skills(all_descriptions)
        skill_to_forecast = scraped_skills[0] if scraped_skills else keyword.title()
        
        st.info(f"Generating a 60-day trend simulation for the skill: **{skill_to_forecast}**")
        
        df_forecast = forecasting.forecast_skill_trend(skill_to_forecast)
        
        # Plotly chart for professional look
        fig = px.line(
            df_forecast, 
            x="date", 
            y="Trend Score", 
            title=f"60-Day Simulated Demand Trend for {skill_to_forecast}",
            labels={"Trend Score": "Relative Demand Score (0-100)"},
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No job data found. Click 'Fetch & Analyze Jobs' to get started.")

# -------------------------------
# PAGE: Analysis History (New Feature)
# -------------------------------
elif page == "Analysis History":
    st.header("Analysis History")
    
    history_df = database.load_history()
    
    if history_df is None or history_df.empty:
        st.info("No previous analysis records found. Run a skill analysis first!")
    else:
        st.subheader(f"Total Records: {len(history_df)}")
        
        # Prepare for display
        display_df = history_df[['timestamp', 'extracted_skills', 'recommendations', 'input_text']].copy()
        display_df.columns = ['Timestamp', 'Extracted Skills', 'Recommended Gaps', 'Input Text Preview']
        
        # Truncate text for cleaner display
        display_df['Input Text Preview'] = display_df['Input Text Preview'].str.slice(0, 100) + '...'
        
        st.dataframe(display_df, use_container_width=True)
        
        st.markdown("---")
        st.caption("Detailed history is stored locally in `data/skills.db`.")


# -------------------------------
# Application Footer
# -------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Project Info:**
    * **Model:** Gemini 2.5 Pro Bono (Simulated)
    * **Architecture:** Forward-Thinking Python
    * **Data:** Local SQLite + CSV/JSON
    * **API:** Free/Open-Source tools only
    """
)
