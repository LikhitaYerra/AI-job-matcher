
# AI Job Matcher 🎯

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

---

## 🌟 Overview

**AI Job Matcher** is a sleek, Streamlit-powered web app designed to help job seekers match their resumes to job postings with precision. Powered by AI (OpenAI's GPT-3.5-turbo), it extracts skills, calculates match scores, and delivers stunning visualizations to guide your career journey. Whether you're scanning a database of jobs or targeting a specific role, this tool has you covered!

---

## ✨ Features

- **Resume Matching** 📄: Upload a PDF resume and compare your skills to job postings.
- **Custom Job Matching** 🎯: Paste a job description for a tailored compatibility check.
- **AI Skill Extraction** 🤖: Uses GPT-3.5-turbo to pull technical skills from resumes and jobs.
- **Visual Insights** 📊: Enjoy gauge charts, word clouds, histograms, and more!
- **Smart Filters** 🔍: Narrow down jobs by location, role level, experience, and more.
- **Skill Breakdown** ✅: See matched and missing skills for every job.
- **Market Trends** 🌍: Explore top skills, job locations, and match distributions.

---

## 🚀 Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Git**: For cloning the repo
- **OpenAI API Key**: Stored in a `.env` file
- **Dependencies**: Listed in `requirements.txt`

### Dependencies

```plaintext
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

### Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/[YourUsername]/AI-Job-Matcher.git
   cd AI-Job-Matcher
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Create a `.env` file in the root directory:
     ```plaintext
     OPENAI_API_KEY=your-api-key-here
     ```

4. **Add Job Data**:
   - Place `processed_jobs.xlsx` in the root directory (see sample format below).

---

## 🎮 Usage

### Launch the App

Run the app locally:
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

### Explore the Features

- **Resume Job Matcher** 📋:
  - Upload your resume.
  - Use sidebar filters (location, role, etc.).
  - View match scores and visualizations.

- **Custom Job Matcher** 🎯:
  - Paste a job description.
  - Upload your resume.
  - Check your match score and skill analysis.

### Sample Job Data Format

| Job Title            | Company Name     | Location     | Technical Skills                | Tools               | Role Level | Experience Required |
|----------------------|------------------|--------------|---------------------------------|---------------------|------------|---------------------|
| Senior Data Scientist| Hopper           | New York, NY | SQL, Pandas, R, machine learning| Tableau, Amplitude | Mid-Level  | 3-5 years          |
| Data Analyst         | Sapphire Digital | Lyndhurst, NJ| SQL, SAS, Python, R            | Excel, PowerBI     | Mid-Level  | 5+ years           |

---

## 📂 Project Structure

```
AI-Job-Matcher/
├── app.py              # Main Streamlit app script
├── processed_jobs.xlsx # Job postings data
├── requirements.txt    # Dependencies list
├── .env               # API key storage
├── LICENSE            # MIT License
└── README.md          # You're reading it!
```

---

## 🛠️ Technical Details

### Core Features

- **Skill Extraction**: GPT-3.5-turbo identifies skills from text.
- **Match Scoring**: `SequenceMatcher` with adjustable thresholds and skill variations.
- **Visualizations**: Plotly for charts, Matplotlib for word clouds, all wrapped in Streamlit.
- **Data Handling**: Pandas for efficient job data processing.

### Limitations

- Requires `processed_jobs.xlsx` to be pre-loaded.
- Needs an OpenAI API key.
- Text-based skill matching (no deep semantic analysis yet).

---

## 🌈 Future Roadmap

### Short-Term
- Support for DOCX resumes 📝
- Better NLP for skill synonyms 🧠
- Faster job data caching ⚡

### Long-Term
- Real-time job scraping 🌐
- User profiles for saved data 💾
- Multi-language support 🌍

---

## 🤝 Contributing

We’d love your help! Here’s how:

1. Fork the repo 🍴
2. Create a branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit changes:
   ```bash
   git commit -m "Add cool feature"
   ```
4. Push:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request 📬

Follow PEP 8 and add tests where possible!

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details:

---

Happy job hunting! 🚀
```
