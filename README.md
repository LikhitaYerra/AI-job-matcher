
# AI Job Matcher

## Overview

**AI Job Matcher** is a Streamlit-based web application designed to help job seekers evaluate how well their resume matches available job postings or custom job descriptions. Leveraging AI-powered skill extraction (via OpenAI's GPT-3.5-turbo), data analysis, and interactive visualizations, this tool provides detailed match scores, skill comparisons, and job market insights. It supports resume uploads in PDF format and processes job data from an Excel file (`processed_jobs.xlsx`), offering filters for location, role level, experience, and more.

The project aims to empower users with actionable insights into their job compatibility while providing an intuitive interface for exploring job opportunities.

## Features

- **Resume Matching**: Upload a PDF resume to compare technical skills against a database of job postings.
- **Custom Job Matching**: Paste a job description to assess resume compatibility with a specific role.
- **Skill Extraction**: Uses OpenAI's GPT-3.5-turbo to extract technical skills from resumes and job descriptions.
- **Interactive Visualizations**: Gauge charts, word clouds, histograms, and bar charts to display match scores and skill distributions.
- **Filters**: Customize job search by location, role level, experience, company size, and industry.
- **Match Insights**: Detailed breakdown of matched and missing skills for each job.
- **Data-Driven Insights**: Analyze job market trends, including top skills, locations, and match score distributions.

## Installation

### Prerequisites

- Python 3.8+
- Git
- An OpenAI API key (stored in a `.env` file)
- Dependencies listed in `requirements.txt`

### Dependencies

```
streamlit>=1.0.0
pandas>=1.5.0
pdfplumber>=0.10.0
openai>=0.27.0
plotly>=5.0.0
wordcloud>=1.8.0
matplotlib>=3.5.0
tqdm>=4.0.0
plotly.express>=0.4.0
scipy>=1.7.0
scikit-learn>=1.0.0
python-dotenv>=0.20.0
```

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/[YourUsername]/AI-Job-Matcher.git
   cd AI-Job-Matcher
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

4. Prepare job data:
   - Place `processed_jobs.xlsx` in the root directory. This file should contain job postings with columns like `Job Title`, `Company Name`, `Location`, `Technical Skills`, `Tools`, etc. (See sample data format below).

## Usage

### Running the Application

1. Launch the Streamlit app:
   ```
   streamlit run app.py
   ```
   *Note*: Replace `app.py` with the actual filename of the provided Python script.

2. Access the app in your browser at `http://localhost:8501`.

### Features in Action

- **Resume Job Matcher Tab**:
  - Upload your resume (PDF).
  - Apply filters (e.g., location, role level) in the sidebar.
  - View match scores, matched/missing skills, and visualizations (e.g., match distribution, top skills).

- **Custom Job Matcher Tab**:
  - Paste a job description.
  - Upload your resume (PDF).
  - See a gauge chart with your match score and a detailed skills comparison.

### Sample Job Data Format

The `processed_jobs.xlsx` file should follow this structure (based on provided sample):

| Job Title            | Company Name      | Location     | Technical Skills                | Tools                | Role Level | Experience Required |
|----------------------|-------------------|--------------|---------------------------------|----------------------|------------|---------------------|
| Senior Data Scientist| Hopper            | New York, NY | SQL, Pandas, R, machine learning| Tableau, Amplitude  | Mid-Level  | 3-5 years          |
| Data Analyst         | Sapphire Digital  | Lyndhurst, NJ| SQL, SAS, Python, R            | Excel, PowerBI      | Mid-Level  | 5+ years           |

## Project Structure

```
AI-Job-Matcher/
├── app.py              # Main Streamlit application script
├── processed_jobs.xlsx # Job postings data (Excel file)
├── requirements.txt    # List of dependencies
├── .env               # Environment variables (e.g., API key)
├── LICENSE            # MIT License file
└── README.md          # Project documentation
```

## Technical Details

### Core Functionality

- **Skill Extraction**: OpenAI's GPT-3.5-turbo extracts skills from resumes and job descriptions, formatted as comma-separated lists.
- **Match Calculation**: Uses `SequenceMatcher` for skill similarity (threshold adjustable via sidebar) and accounts for skill variations (e.g., "SQL" ≈ "database").
- **Visualizations**: Built with Plotly (gauge charts, histograms), Matplotlib (word clouds), and Streamlit for interactivity.
- **Data Processing**: Pandas handles job data, with filtering and sorting based on user inputs.

### Limitations

- Requires `processed_jobs.xlsx` to be pre-populated with job data.
- OpenAI API key is mandatory for skill extraction.
- Current skill matching is text-based; semantic understanding is limited.

## Future Development

### Short-Term Goals
- Add support for more resume formats (e.g., DOCX).
- Enhance skill matching with NLP for better synonym recognition.
- Implement caching for faster job data loading.

### Long-Term Vision
- Integrate real-time job scraping from online sources.
- Add user profiles to save resumes and preferences.
- Expand to support multiple languages and regions.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

Please ensure your code follows PEP 8 style guidelines and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details:

