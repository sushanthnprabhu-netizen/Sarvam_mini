import hashlib

import pandas as pd
import streamlit as st

from sarvam_client import detect_language, extract, next_probe, speak, transcribe
from stats_engine import analyze

st.set_page_config(page_title="BhashaLab", layout="wide")
st.title("BhashaLab: code-mixed field research engine")

DEFAULT_HYP = "Small shopkeepers prefer UPI credit lines over traditional micro-loans"
DEFAULT_OPENER = "Namaste! In your own words, how do you manage when your shop suddenly needs cash?"

ss = st.session_state
ss.setdefault("respondents", [{"turns": [], "english": [], "record": None}])
ss.setdefault("current", 0)
ss.setdefault("last_audio", None)
ss.setdefault("probe_audio", None)

with st.sidebar:
    hypothesis = st.text_area("Hypothesis", DEFAULT_HYP)
    opener = st.text_area("Opening question", DEFAULT_OPENER)
    mu0 = st.number_input("Neutral score (H0 mean)", 1.0, 5.0, 3.0, 0.5)
    if st.button("Next respondent"):
        ss.respondents.append({"turns": [], "english": [], "record": None})
        ss.current = len(ss.respondents) - 1
        ss.probe_audio = None
        st.rerun()

resp_now = ss.respondents[ss.current]


def process(original: str, english: str, lang: str):
    resp_now["turns"].append({"role": "user", "content": original})
    resp_now["english"].append(english)
    full_orig = "\n".join(t["content"] for t in resp_now["turns"] if t["role"] == "user")
    full_eng = "\n".join(resp_now["english"])
    resp_now["record"] = extract(hypothesis, full_orig, full_eng)
    probe = next_probe(hypothesis, opener, resp_now["turns"], lang)
    resp_now["turns"].append({"role": "assistant", "content": probe})
    try:
        ss.probe_audio = speak(probe, lang)
    except Exception as e:
        ss.probe_audio = None
        st.warning(f"Voice playback failed: {e}")


left, right = st.columns(2)

with left:
    st.subheader(f"Respondent {ss.current + 1}")
    st.info(opener)
    for t in resp_now["turns"]:
        st.chat_message("assistant" if t["role"] == "assistant" else "user").write(t["content"])
    if ss.probe_audio:
        st.audio(ss.probe_audio, format="audio/wav", autoplay=True)

    tab_voice, tab_text = st.tabs(["Speak", "Type (no mic)"])
    with tab_voice:
        audio = st.audio_input("Record the answer")
        if audio is not None:
            data = audio.getvalue()
            h = hashlib.md5(data).hexdigest()
            if h != ss.last_audio:
                ss.last_audio = h
                try:
                    with st.spinner("Transcribing and scoring..."):
                        original, lang = transcribe(data, "codemix")
                        english, _ = transcribe(data, "translate")
                        lang = lang if lang and lang != "unknown" else detect_language(original)
                        process(original, english, lang)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
    with tab_text:
        typed = st.text_area("Type the answer (any Indic language or Hinglish)")
        if st.button("Submit answer") and typed.strip():
            try:
                with st.spinner("Scoring..."):
                    process(typed.strip(), typed.strip(), detect_language(typed))
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

with right:
    st.subheader("Live analysis")
    rows = [{"respondent": i + 1, **r["record"]}
            for i, r in enumerate(ss.respondents) if r["record"]]
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df["likert"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0))
        res = analyze(df["likert"].tolist(), mu0=mu0)
        if res is None:
            st.info("Need at least 2 respondents with differing scores to run the test.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("n", res.n)
            c2.metric("Mean score", f"{res.mean:.2f}")
            c3.metric("p-value", f"{res.p:.4f}")
            c4, c5, c6 = st.columns(3)
            c4.metric("95% CI", f"{res.ci_low:.2f} to {res.ci_high:.2f}")
            c5.metric("Power", f"{res.power:.0%}")
            c6.metric("More needed (80% power)",
                      "n/a" if res.remaining is None else res.remaining)
            st.caption("One-sample t-test of Likert scores against the neutral value. "
                       "Sample-size estimate uses the observed effect size, so treat it as rough.")
    else:
        st.write("Answer the first question to see results.")