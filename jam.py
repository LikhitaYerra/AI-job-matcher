import streamlit as st
import pandas as pd
import pdfplumber
import openai
from difflib import SequenceMatcher
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_requirements_from_text(text):
    """Extract requirements from custom job description"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": f"""
                Extract all technical requirements from this job description.
                Include:
                - Required technical skills
                - Tools and technologies
                - Programming languages
                - Frameworks and platforms
                
                Format the output as a comma-separated list like this:
                Skills: skill1, skill2, skill3

                Job Description:
                {text}
                """
            }],
            max_tokens=300,
            temperature=0.0
        )
        
        content = response['choices'][0]['message']['content']
        for line in content.split('\n'):
            if line.lower().startswith('skills:'):
                skills_text = line[7:].strip()
                skills_list = [skill.strip() for skill in skills_text.split(',')]
                return [s for s in skills_list if s]
        return []
        
    except Exception as e:
        st.error(f"Error extracting requirements: {str(e)}")
        return []

def display_gauge_chart(score):
    """Create a gauge chart for the match score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Match Score"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    return fig

# Load processed jobs data
@st.cache_data
def load_job_data():
    """Load preprocessed job data"""
    try:
        # Use relative path instead of absolute path
        file_path = "processed_jobs.xlsx"  # Ensure this file is in the same directory as your script
        if not os.path.exists(file_path):
            st.error(f"File not found at {file_path}")
            return None
        df = pd.read_excel(file_path)
        # Clean Role Level column
        df['Role Level'] = df['Role Level'].fillna('Not Specified').astype(str)
        return df
    except Exception as e:
        st.error(f"Error loading job data: {str(e)}")
        return None

def extract_skills_from_resume(pdf_file, api_key):
    """Extract skills from resume using GPT-3.5"""
    try:
        # Read PDF content
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        # Configure OpenAI
        openai.api_key = api_key
        
        # Create prompt for skills extraction
        prompt = f"""
        Find the SKILLS or TECHNICAL SKILLS section in this resume and extract all technical items.
        
        Focus on extracting:
        - Programming languages (e.g., Python, Java)
        - Database technologies (e.g., SQL, MongoDB)
        - Tools and software (e.g., Tableau, Excel)
        - Frameworks and libraries
        - Technical platforms
        - Analysis tools
        
        Format the output as:
        SKILLS: skill1, skill2, skill3

        Important:
        - Only extract skills that are explicitly mentioned
        - Include ALL technical items listed in the skills section
        - Separate skills with commas
        - Keep the exact names as written
        - Don't add skills not present in the resume
        
        Resume text:
        {text}
        """

        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user", 
                "content": prompt
            }],
            max_tokens=500,
            temperature=0.0
        )

        # Parse skills from response
        content = response['choices'][0]['message']['content']
        skills = []
        
        for line in content.split('\n'):
            if line.lower().startswith('skills:'):
                # Clean and format skills
                skills_text = line[7:].strip()
                skills = [skill.strip() for skill in skills_text.split(',')]
                # Remove empty strings and duplicates while preserving order
                skills = list(dict.fromkeys([s for s in skills if s and len(s) > 1]))
                
                
                return skills

        if not skills:  # If no skills were found with the SKILLS: prefix
            # Try to find any comma-separated list in the response
            text_chunks = content.split(',')
            if text_chunks:
                skills = [chunk.strip() for chunk in text_chunks]
                skills = list(dict.fromkeys([s for s in skills if s and len(s) > 1]))
                
                # Debug output
                st.write("Debug - Extracted Skills (alternative method):", skills)
                return skills
        
        return []

    except Exception as e:
        st.error(f"Error extracting skills from resume: {str(e)}")
        return []

def calculate_match(job_requirements: dict, resume_skills: list, threshold: float = 0.8) -> tuple:
    """Calculate match score and identify matching and missing requirements"""
    if not job_requirements or not resume_skills:
        return 0, [], []
    
    # Normalize all skills to lowercase for better matching
    job_reqs = []
    tech_skills = job_requirements.get('Technical Skills', '')
    if isinstance(tech_skills, str) and tech_skills.strip():
        # Split and clean job requirements
        job_reqs = [req.strip().lower() for req in tech_skills.split(',') if req.strip()]
    
    resume_reqs = [skill.strip().lower() for skill in resume_skills if skill.strip()]
    
    # Define common variations and related terms
    skill_variations = {
        'sql': ['sql', 'database', 'relational database', 'dbms'],
        'python': ['python', 'python programming'],
        'data visualization': ['data visualization', 'visualization', 'tableau'],
        'data analysis': ['data analysis', 'analysis', 'analytics', 'project analytics'],
        'machine learning': ['machine learning', 'ml', 'deep learning', 'ai'],
    }
    
    # Find matches using improved similarity checking
    matched_reqs = []
    for r_skill in resume_reqs:
        # Check for direct matches or variations
        for j_skill in job_reqs:
            # Direct match check
            if r_skill == j_skill:
                matched_reqs.append(r_skill)
                continue
                
            # Check variations
            for base_skill, variations in skill_variations.items():
                if r_skill in variations and j_skill in variations:
                    matched_reqs.append(j_skill)
                    break
            
            # If no direct or variation match, check similarity
            similarity = SequenceMatcher(None, r_skill, j_skill).ratio()
            if similarity >= threshold:
                matched_reqs.append(j_skill)
    
    # Remove duplicates while preserving order
    matched_reqs = list(dict.fromkeys(matched_reqs))
    
    # Calculate match score
    match_score = len(matched_reqs) / len(job_reqs) * 100 if job_reqs else 0
    
    # Identify missing requirements
    missing_reqs = [req for req in job_reqs if req not in matched_reqs]
    
    return match_score, matched_reqs, missing_reqs

def create_wordcloud(requirements):
    """Create a word cloud from technical requirements"""
    if not requirements:
        return None
        
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis',
        prefer_horizontal=0.7
    ).generate(' '.join(requirements))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

def create_match_distribution_chart(match_scores):
    """Create a distribution chart of match scores"""
    fig = px.histogram(
        match_scores,
        x="Match Score",
        nbins=20,
        title="Distribution of Job Match Scores",
        labels={"Match Score": "Match Score (%)", "count": "Number of Jobs"},
        color_discrete_sequence=['#3366CC']
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white'
    )
    return fig

def create_top_skills_chart(matches):
    """Create a chart of most common required skills"""
    all_skills = []
    for match in matches:
        if "All Requirements" in match:
            skills = [s.strip() for s in str(match["All Requirements"]).split(",")]
            all_skills.extend(skills)
    
    skill_counts = Counter(all_skills).most_common(10)
    
    fig = px.bar(
        x=[skill[0] for skill in skill_counts],
        y=[skill[1] for skill in skill_counts],
        title="Top 10 Most Required Technical Skills",
        labels={"x": "Skill", "y": "Frequency"},
        color_discrete_sequence=['#3366CC']
    )
    fig.update_layout(
        plot_bgcolor='white',
        xaxis_tickangle=-45
    )
    return fig

def create_location_chart(matches):
    """Create a chart of job locations"""
    location_counts = Counter([match["Location"] for match in matches]).most_common()
    
    fig = px.pie(
        values=[count for _, count in location_counts],
        names=[loc for loc, _ in location_counts],
        title="Job Distribution by Location",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def display_match_results(matches):
    """Display the match results in a table format"""
    # Convert matches to a DataFrame for better visualization
    matches_df = pd.DataFrame(matches)
    st.dataframe(matches_df)

def main():
    st.set_page_config(
        page_title="AI Job Matcher",
        page_icon="🎯",
        layout="wide"
    )
    
    # Custom CSS for header
    st.markdown("""
        <style>
        .header-container {
            display: flex;
            align-items: center;
            padding: 1rem 0;
        }
        .header-icon {
            font-size: 3rem;
            margin-right: 1rem;
        }
        .header-title {
            font-size: 2.5rem;
            font-weight: bold;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create styled header
    st.markdown("""
        <div class="header-container">
            <div class="header-icon">🤖</div>
            <h1 class="header-title">AI Resume Matcher</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("Upload your resume to find matching jobs!")
    
    # Create tabs
    tab1, tab2 = st.tabs(["📋 Resume Job Matcher", "🎯 Custom Job Matcher"])
    
    with tab1:
        st.title("AI Resume Matcher")
        st.write("Upload your resume to find matching jobs!")
        
        # Load job data
        jobs_df = load_job_data()
        if jobs_df is None:
            return

        # Create single metrics placeholder at the top
        metrics_container = st.empty()

        # Display initial metrics
        with metrics_container.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Jobs Available", len(jobs_df))
            with col2:
                st.metric("Strong Matches (≥50%)", 0)
            with col3:
                st.metric("Potential Matches (<50%)", 0)

        # File upload
        resume_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf")
        
        # Sidebar configuration
        st.sidebar.title("Search and Filter Settings")
        
        # Matching threshold
        st.sidebar.subheader("Matching Criteria")
        similarity_threshold = st.sidebar.slider(
            "Skill Matching Threshold", 
            min_value=0.5, 
            max_value=1.0, 
            value=0.8,
            help="Minimum similarity score for skills matching"
        )
        
        min_match_score = st.sidebar.slider(
            "Minimum Match Score (%)", 
            min_value=0, 
            max_value=100, 
            value=30,
            help="Minimum match score to display job"
        )

        # Location filter
        st.sidebar.subheader("Location Filter")
        all_locations = sorted(jobs_df['Location'].unique())
        selected_locations = st.sidebar.multiselect(
            "Select Locations",
            all_locations,
            default=[]
        )

        # Role level filter
        st.sidebar.subheader("Role Level")
        all_levels = sorted(jobs_df['Role Level'].unique())
        selected_levels = st.sidebar.multiselect(
            "Select Role Levels",
            all_levels,
            default=[]
        )

        # Experience filter
        st.sidebar.subheader("Experience Range")
        max_exp = st.sidebar.number_input(
            "Maximum Years of Experience",
            min_value=0,
            max_value=20,
            value=20
        )

        # Company size filter
        st.sidebar.subheader("Company Size")
        all_sizes = sorted(jobs_df['Size'].unique())
        selected_sizes = st.sidebar.multiselect(
            "Select Company Sizes",
            all_sizes,
            default=[]
        )

        # Industry filter
        st.sidebar.subheader("Industry")
        all_industries = sorted(jobs_df['Industry'].unique())
        selected_industries = st.sidebar.multiselect(
            "Select Industries",
            all_industries,
            default=[]
        )

        # Number of results filter
        st.sidebar.subheader("Results Limit")
        n_results = st.sidebar.selectbox(
            "Show Top N Results",
            options=[10, 20, 30, 50, 100],
            index=0,
            help="Limit the number of job matches shown"
        )

        if resume_file:
            with st.spinner("Analyzing your resume..."):
                resume_requirements = extract_skills_from_resume(
                    resume_file,
                    os.getenv("OPENAI_API_KEY")
                )
                
                if resume_requirements:
                    # Display technical profile
                    st.header("Your Profile")
                    profile_col1, profile_col2 = st.columns([2, 1])
                    
                    with profile_col1:
                        st.subheader("Technical Requirements")
                        st.write(", ".join(resume_requirements))
                    
                    with profile_col2:
                        wordcloud_fig = create_wordcloud(resume_requirements)
                        if wordcloud_fig:
                            st.pyplot(wordcloud_fig)

                    # Calculate matches
                    matches = []
                    match_scores = []
                    
                    for _, job in jobs_df.iterrows():
                        # Apply filters
                        if (selected_locations and job['Location'] not in selected_locations or
                            selected_levels and job['Role Level'] not in selected_levels or
                            selected_sizes and job['Size'] not in selected_sizes or
                            selected_industries and job['Industry'] not in selected_industries):
                            continue

                        # Check experience requirement
                        try:
                            exp_required = float(str(job['Experience Required']).split()[0])
                            if exp_required > max_exp:
                                continue
                        except:
                            pass

                        score, matched_reqs, missing_reqs = calculate_match(
                            {
                                'Technical Skills': job['Technical Skills'],
                                'Tools': job['Tools']
                            },
                            resume_requirements,
                            similarity_threshold
                        )
                        
                        match_scores.append({"Match Score": score})
                        
                        if score >= min_match_score:
                            matches.append({
                                "Job Title": job["Job Title"],
                                "Company": job["Company Name"],
                                "Location": job["Location"],
                                "Match Score": score,
                                "Matched Requirements": matched_reqs,
                                "Missing Requirements": missing_reqs,
                                "All Requirements": f"{job['Technical Skills']}, {job['Tools']}",
                                "Experience": job["Experience Required"],
                                "Role Level": job["Role Level"],
                                "Salary Estimate": job["Salary Estimate"],
                                "Industry": job["Industry"],
                                "Size": job["Size"],
                                "Description": job.get("Job Description", "No description available")
                            })
                    
                    # Update metrics ONLY ONCE after calculations
                    matches_above_50 = len([m for m in matches if m["Match Score"] >= 50])
                    matches_below_50 = len([m for m in matches if m["Match Score"] < 50])
                    
                    # Update the metrics using the same container
                    with metrics_container.container():
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Jobs Available", len(jobs_df))
                        with col2:
                            st.metric("Strong Matches (≥50%)", matches_above_50)
                        with col3:
                            st.metric("Potential Matches (<50%)", matches_below_50)

                    if matches:
                        # Sort and limit matches
                        matches.sort(key=lambda x: x["Match Score"], reverse=True)
                        matches = matches[:n_results]
                        
                        # Add spacing before results
                        st.markdown("---")
                        
                        # Create visualization layout
                        st.header("Job Market Analysis")
                        viz_col1, viz_col2 = st.columns(2)
                        
                        with viz_col1:
                            st.plotly_chart(create_match_distribution_chart(pd.DataFrame(match_scores)))
                            st.plotly_chart(create_location_chart(matches))
                        
                        with viz_col2:
                            st.plotly_chart(create_top_skills_chart(matches))
                        
                        # Display matching jobs
                        st.markdown("---")
                        st.header(f"Found {len(matches)} Matching Jobs")
                        
                        for match in matches:
                            with st.expander(
                                f"🎯 {match['Match Score']:.1f}% Match - {match['Job Title']} at {match['Company']}"
                            ):
                                # Job Overview
                                st.markdown("""---""")
                                st.markdown("### Job Overview")
                                cols = st.columns([2, 1])
                                
                                with cols[0]:
                                    st.markdown("**Job Description**")
                                    description = match.get('Description', 'No description available')
                                    st.write(description if description else "No description available")
                                
                                with cols[1]:
                                    st.markdown("**Company Details**")
                                    st.write(f"📍 Location: {match['Location']}")
                                    st.write(f"💼 Role Level: {match['Role Level']}")
                                    st.write(f"⏳ Experience: {match['Experience']}")
                                    if pd.notna(match['Salary Estimate']):
                                        st.write(f"💰 Salary: {match['Salary Estimate']}")
                                    st.write(f"🏢 Company Size: {match['Size']}")
                                    st.write(f"🏭 Industry: {match['Industry']}")
                                
                                # Skills Analysis
                                st.markdown("""---""")
                                st.markdown("### Skills Analysis")
                                skill_cols = st.columns(2)
                                
                                with skill_cols[0]:
                                    st.markdown("**✅ Matched Requirements**")
                                    for skill in match['Matched Requirements']:
                                        st.markdown(f"- {skill}")
                                
                                with skill_cols[1]:
                                    if match['Missing Requirements']:
                                        st.markdown("**🎯 Skills to Develop**")
                                        for skill in match['Missing Requirements']:
                                            st.markdown(f"- {skill}")
                                
                                # Add visual match indicator
                                st.markdown("""---""")
                                progress_cols = st.columns([3, 1])
                                with progress_cols[0]:
                                    st.progress(match['Match Score']/100)
                                with progress_cols[1]:
                                    st.write(f"**{match['Match Score']:.1f}%** match")

                    else:
                        st.warning(
                            "No matching jobs found. Try adjusting the filters or matching criteria."
                        )

    with tab2:
        st.title("Custom Job Description Matcher")
        st.write("🎯 Want to see how well you match with a specific job? Paste the job description below!")
        
        job_description = st.text_area(
            "Paste Job Description",
            height=300,
            placeholder="Paste the complete job description here..."
        )
        
        custom_resume_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", key="custom_matcher")
        
        if job_description and custom_resume_file:
            with st.spinner("Analyzing match..."):
                # Extract requirements from job description
                job_reqs = extract_requirements_from_text(job_description)
                
                # Extract skills from resume
                resume_skills = extract_skills_from_resume(
                    custom_resume_file,
                    os.getenv("OPENAI_API_KEY")
                )
                
                if resume_skills and job_reqs:
                    # Calculate match
                    match_score, matched_reqs, missing_reqs = calculate_match(
                        {'Technical Skills': ', '.join(job_reqs)},
                        resume_skills,
                        similarity_threshold
                    )
                    
                    # Display results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Match Analysis")
                        gauge_chart = display_gauge_chart(match_score)
                        st.plotly_chart(gauge_chart)
                        
                    with col2:
                        st.subheader("Skills Analysis")
                        st.write(" Matched Skills:")
                        st.write(", ".join(matched_reqs))
                        if missing_reqs:
                            st.write("🎯 Skills to Develop:")
                            st.write(", ".join(missing_reqs))

if __name__ == "__main__":
    main()