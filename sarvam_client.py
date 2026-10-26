import base64
import io
import json
import os
from pathlib import Path

from sarvamai import SarvamAI

TTS_LANGS = {"hi-IN", "bn-IN", "ta-IN", "te-IN", "kn-IN", "ml-IN",
             "mr-IN", "gu-IN", "pa-IN", "od-IN", "en-IN"}


def _load_env():
    path = Path(__file__).parent / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_env()
_client = None


def get_client():
    global _client
    if _client is None:
        key = os.environ.get("SARVAM_API_KEY")
        if not key:
            raise RuntimeError("SARVAM_API_KEY is empty. Paste your key into .env first.")
        _client = SarvamAI(api_subscription_key=key)
    return _client


def transcribe(audio_bytes: bytes, mode: str):
    """mode: 'codemix' keeps the original speech; 'translate' gives English."""
    f = io.BytesIO(audio_bytes)
    f.name = "answer.wav"
    resp = get_client().speech_to_text.transcribe(file=f, model="saaras:v4", mode=mode)
    return resp.transcript, getattr(resp, "language_code", None)


def detect_language(text: str, fallback: str = "hi-IN") -> str:
    try:
        code = get_client().text.identify_language(input=text[:1000]).language_code
        return code or fallback
    except Exception:
        return fallback


def extract(hypothesis: str, original: str, english: str) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "likert": {"type": "integer"},
            "stance": {"type": "string", "enum": ["supports", "opposes", "mixed", "unclear"]},
            "sentiment": {"type": "number"},
            "theme": {"type": "string"},
            "evidence": {"type": "string"},
        },
        "required": ["likert", "stance", "sentiment", "theme", "evidence"],
        "additionalProperties": False,
    }
    prompt = (
        f"Hypothesis being tested: {hypothesis}\n\n"
        "Read the respondent's words and score them.\n"
        "- likert: 1 = strongly contradicts the hypothesis, 3 = neutral/unclear, 5 = strongly supports it.\n"
        "- sentiment: -1.0 (very negative) to 1.0 (very positive).\n"
        "- theme: the main reason they gave, in 1 to 4 words (English).\n"
        "- evidence: one short English phrase from their answer that justifies the score.\n\n"
        f"Original: {original}\n\nEnglish translation: {english}"
    )
    resp = get_client().chat.completions(
        model="sarvam-105b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema",
                         "json_schema": {"name": "survey_extraction", "strict": True, "schema": schema}},
        reasoning_effort=None,
        max_tokens=600,
    )
    data = json.loads(resp.choices[0].message.content)
    data["likert"] = max(1, min(5, int(data["likert"])))
    data["sentiment"] = max(-1.0, min(1.0, float(data["sentiment"])))
    return data


def next_probe(hypothesis: str, opener: str, turns: list, lang: str) -> str:
    system = (
        "You are a warm, neutral field-survey interviewer. "
        f"The study topic is: {hypothesis}. Never reveal or hint at the hypothesis or lead the respondent. "
        "Ask exactly ONE short follow-up question (under 25 words) that digs into their reason or an example. "
        "Reply in the same language and script the respondent used, matching their code-mixing."
    )
    messages = [{"role": "system", "content": system},
                {"role": "assistant", "content": opener}] + turns
    resp = get_client().chat.completions(
        model="sarvam-105b-conversations",
        messages=messages,
        reasoning_effort=None,
        max_tokens=300,
    )
    return resp.choices[0].message.content.strip()


def speak(text: str, lang: str) -> bytes:
    lang = lang if lang in TTS_LANGS else "en-IN"
    resp = get_client().text_to_speech.convert(
        text=text, language_code=lang, model="bulbul:v4-flash"
    )
    return base64.b64decode("".join(resp.audios))