# BhashaLab — Code-Mixed Field Research Engine

**Turn natural conversations in Indian languages into structured survey data and statistical insights.**

BhashaLab is an AI-powered field research prototype that helps researchers conduct conversational surveys in English, Hinglish, Kannada, Hindi, Tamil, Telugu, and other supported languages.

Instead of forcing respondents into rigid multiple-choice questions, BhashaLab accepts natural spoken or typed answers, extracts structured research variables, and presents statistical summaries through an interactive dashboard.

## Features

- **Multilingual speech transcription:** Convert recorded responses into text using Sarvam's Saaras speech-to-text API.
- **Code-mixed language support:** Preserve the original transcript while obtaining an English translation for analysis.
- **AI-powered response extraction:** Use Sarvam's language models to extract Likert scores, sentiment, themes, respondent stance, and supporting evidence.
- **Adaptive follow-up questions:** Generate neutral follow-up questions that encourage respondents to explain their answers.
- **Voice-based interaction:** Generate spoken follow-up questions using Sarvam's text-to-speech API.
- **Live statistical dashboard:** Display response distributions, sample means, p-values, 95% confidence intervals, and estimated statistical power.
- **Text input fallback:** Test the research workflow without a microphone.

## Technology Stack

- Python
- Sarvam AI Python SDK (`sarvamai`)
- Streamlit
- Pandas
- SciPy

## Architecture

```text
Respondent
    |
    v
Voice Recording / Text Input
    |
    v
Sarvam Saaras Speech-to-Text
    |
    +--> Original Transcript
    |
    +--> English Translation
    |
    v
Sarvam Language Model
    |
    +--> Likert Score
    +--> Sentiment
    +--> Research Theme
    +--> Supporting Evidence
    |
    v
Follow-up Question Generation
    |
    v
Sarvam Text-to-Speech
    |
    v
Interactive Streamlit Dashboard
    |
    +--> Response Distribution
    +--> Mean Score
    +--> Hypothesis Test
    +--> Confidence Interval
    +--> Statistical Power Estimate
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sushanthnprabhu-netizen/Sarvam_mini.git
cd Sarvam_mini
```

### 2. Create a virtual environment (recommended)

Windows PowerShell:

```powershell
python
