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
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
SARVAM_API_KEY=your_actual_api_key
```

Replace the placeholder with your Sarvam API key. Never commit `.env` or expose your API key in source code, screenshots, or logs.

Ensure `.env` is listed in `.gitignore`.

### 5. Test the Sarvam connection

```bash
python main.py
```

The script should print the response returned by `sarvam-105b-conversations` when your API key, model access, SDK, and network connection are configured correctly.

### 6. Launch BhashaLab

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal. Start with the text-input interface, then try voice recording if supported by your environment.

## Statistical Analysis

BhashaLab currently uses a one-sample t-test to compare extracted Likert scores against a configurable neutral reference value.

The dashboard is designed to report:

- Sample size and mean score
- Standard deviation
- Test statistic and p-value
- 95% confidence interval
- Estimated statistical power
- Approximate additional sample size needed to reach a target power

**Research limitation:** These results depend on the quality and consistency of AI-extracted scores. Likert scores are ordinal, and a t-test may not be appropriate for every research design. Sample-size estimates are approximate and should be validated before drawing research conclusions.

## Security

- Store API credentials in `.env` or your deployment platform's secret manager.
- Keep `.env` out of version control.
- Never print or commit API keys.
- Collect consent before recording respondents.
- Protect transcripts and research data, especially when they contain personal information.

## Current Project Status

BhashaLab is an experimental prototype. The individual API integrations, audio response handling, and statistical calculations must be tested in the target environment before the complete workflow can be considered verified.

## Roadmap

- [ ] Verify the first Sarvam chat completion.
- [ ] Validate transcription and translation.
- [ ] Test structured response extraction.
- [ ] Validate follow-up generation and speech synthesis.
- [ ] Improve statistical methodology and sample-size estimation.
- [ ] Add persistent respondent records and downloadable research results.
- [ ] Deploy the dashboard securely.

## License

Choose a license before distributing or accepting external contributions to the project.
