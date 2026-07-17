"""
Spam Detector — Streamlit frontend
Loads model/voting_model.pkl (produced by spamdetector_corrected.ipynb) and
lets someone paste a message in to see how the three-model ensemble votes.

Run with:  streamlit run app.py
"""

import html
import pickle
from pathlib import Path

import streamlit as st

MODEL_PATH = Path("model/voting_model.pkl")

# ----------------------------------------------------------------------------
# Page setup
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Spam Detector", page_icon="📡", layout="wide")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #0D1614;
    --panel: #16221F;
    --panel-2: #1C2A26;
    --line: #2A3733;
    --text: #E7E2D6;
    --muted: #8B9A96;
    --amber: #E8A33D;
    --amber-dim: #3A2E1B;
    --mint: #4FD8B0;
    --mint-dim: #16302A;
}

html, body, .stApp { background: var(--bg) !important; color: var(--text); }
.stApp { font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 880px; margin: 0 auto; padding: 3rem 1.5rem 4rem; }

/* ---- header ---- */
.eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.16em;
    color: var(--mint);
    margin-bottom: 10px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: clamp(30px, 5vw, 46px);
    line-height: 1.05;
    margin: 0 0 10px;
    color: var(--text);
}
.hero-sub {
    font-family: 'IBM Plex Sans', sans-serif;
    font-size: 16px;
    color: var(--muted);
    max-width: 52ch;
    margin-bottom: 8px;
}
hr.divider { border: none; border-top: 1px solid var(--line); margin: 28px 0; }

/* ---- panels ---- */
.panel-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.12em;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ---- textarea ---- */
.stTextArea textarea {
    background: var(--panel) !important;
    color: var(--text) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;
}
.stTextArea textarea:focus { border-color: var(--mint) !important; box-shadow: 0 0 0 1px var(--mint) !important; }
.stTextArea textarea::placeholder { color: var(--muted) !important; }

/* ---- buttons ---- */
.stButton > button {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.03em;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: var(--panel);
    color: var(--text);
    padding: 0.5rem 1rem;
    transition: border-color 0.15s ease;
}
.stButton > button:hover { border-color: var(--mint); color: var(--mint); }
.stButton > button:focus-visible { outline: 2px solid var(--mint); outline-offset: 2px; }
.stButton > button[kind="primary"] {
    background: var(--mint-dim);
    border: 1px solid var(--mint);
    color: var(--mint);
    font-weight: 600;
}
.stButton > button[kind="primary"]:hover { background: var(--mint); color: var(--bg); }

/* ---- verdict badge ---- */
.verdict { text-align: center; padding: 30px 20px; border-radius: 14px; border: 1px solid var(--line); margin-bottom: 18px; }
.verdict.spam { background: linear-gradient(180deg, var(--amber-dim), var(--panel)); border-color: var(--amber); }
.verdict.ham  { background: linear-gradient(180deg, var(--mint-dim), var(--panel));  border-color: var(--mint); }
.verdict.idle { background: var(--panel); }
.verdict-label {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: clamp(24px, 6vw, 34px);
    letter-spacing: 0.01em;
}
.verdict.spam .verdict-label { color: var(--amber); }
.verdict.ham  .verdict-label { color: var(--mint); }
.verdict.idle .verdict-label { color: var(--muted); font-family: 'IBM Plex Mono', monospace; font-size: 15px; letter-spacing: 0.1em; }
.verdict-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: var(--muted);
    margin-top: 8px;
    letter-spacing: 0.05em;
}

/* ---- sensor lights ---- */
.sensor-row { display: flex; flex-direction: column; gap: 8px; margin: 4px 0 20px; }
.sensor { display: flex; align-items: center; gap: 12px; padding: 11px 14px; border: 1px solid var(--line); border-radius: 8px; background: var(--panel-2); }
.sensor-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; background: var(--line); }
.sensor.spam .sensor-dot { background: var(--amber); box-shadow: 0 0 6px var(--amber); }
.sensor.ham  .sensor-dot { background: var(--mint);  box-shadow: 0 0 6px var(--mint); }
@media (prefers-reduced-motion: no-preference) {
    .sensor.spam .sensor-dot { animation: pulse-amber 2.2s ease-in-out infinite; }
    .sensor.ham  .sensor-dot { animation: pulse-mint 2.2s ease-in-out infinite; }
}
@keyframes pulse-amber { 0%,100% { box-shadow: 0 0 6px var(--amber); } 50% { box-shadow: 0 0 15px var(--amber); } }
@keyframes pulse-mint  { 0%,100% { box-shadow: 0 0 6px var(--mint); }  50% { box-shadow: 0 0 15px var(--mint); } }
.sensor-label { font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 0.06em; color: var(--muted); flex: 1; }
.sensor-verdict { font-family: 'IBM Plex Mono', monospace; font-size: 12px; font-weight: 600; color: var(--muted); }
.sensor.spam .sensor-verdict { color: var(--amber); }
.sensor.ham  .sensor-verdict { color: var(--mint); }

/* ---- term chips ---- */
.term-chip {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    padding: 4px 11px;
    border-radius: 999px;
    margin: 3px 6px 3px 0;
    border: 1px solid;
}
.term-chip.spam { color: var(--amber); border-color: var(--amber); background: var(--amber-dim); }
.term-chip.ham  { color: var(--mint);  border-color: var(--mint);  background: var(--mint-dim); }

/* ---- footer note ---- */
.footnote { font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: var(--muted); line-height: 1.7; }
.footnote b { color: var(--text); }
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Model loading
# ----------------------------------------------------------------------------
@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


model_loaded = MODEL_PATH.exists()
if model_loaded:
    model_data = load_model()
    voting_model = model_data["model"]
    vectorizer = model_data["vectorizer"]
    vocab_size = len(model_data.get("features", vectorizer.get_feature_names_out()))

MODEL_NAMES = {"lr": "Logistic Regression", "nb": "Naive Bayes", "svm": "Linear SVM"}

EXAMPLES = {
    "Prize scam": "Congratulations! You've WON a $1000 gift card. Click here to claim now: bit.ly/claim-prize",
    "Casual text": "Hey, are we still on for lunch tomorrow at noon?",
    "Account alert": "URGENT: Your account has been suspended. Verify your identity immediately to avoid closure.",
}

# ----------------------------------------------------------------------------
# Prediction logic
# ----------------------------------------------------------------------------
def get_signal_terms(text, top_n=5):
    """Uses the LR sub-model's coefficients to explain which words/bigrams in
    this specific message pushed the vote toward spam or toward ham."""
    vec = vectorizer.transform([text])
    lr = voting_model.named_estimators_["lr"]
    coefs = lr.coef_[0]
    feature_names = vectorizer.get_feature_names_out()
    nz = vec.nonzero()[1]
    contributions = [(feature_names[i], vec[0, i] * coefs[i]) for i in nz]
    contributions.sort(key=lambda t: t[1], reverse=True)
    spam_terms = [t[0] for t in contributions if t[1] > 0][:top_n]
    ham_terms = [t[0] for t in contributions if t[1] < 0][-top_n:]
    return spam_terms, ham_terms


def run_prediction(text):
    vec = vectorizer.transform([text])
    final_pred = int(voting_model.predict(vec)[0])
    sub_preds = {name: int(est.predict(vec)[0]) for name, est in voting_model.named_estimators_.items()}
    spam_terms, ham_terms = get_signal_terms(text)
    return {"final": final_pred, "sub": sub_preds, "spam_terms": spam_terms, "ham_terms": ham_terms}


# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "message_text" not in st.session_state:
    st.session_state.message_text = ""
if "result" not in st.session_state:
    st.session_state.result = None


def set_example(text):
    st.session_state.message_text = text
    st.session_state.result = None


# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="eyebrow">SIGNAL ANALYSIS · SMS / EMAIL</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Spam Detector</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Three classifiers vote on every message. Paste one in and see how they call it.</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

if not model_loaded:
    st.markdown(
        f"""
        <div class="verdict idle">
            <div class="verdict-label">NO TRAINED MODEL FOUND</div>
            <div class="verdict-sub">Run spamdetector_corrected.ipynb first to produce {MODEL_PATH.as_posix()},
            then reload this page.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ----------------------------------------------------------------------------
# Main layout
# ----------------------------------------------------------------------------
col_input, col_result = st.columns([1, 1], gap="large")

with col_input:
    st.markdown('<div class="panel-label">Message</div>', unsafe_allow_html=True)
    st.text_area(
        "Message",
        key="message_text",
        height=160,
        label_visibility="collapsed",
        placeholder="Paste a message to scan…",
    )

    st.markdown('<div class="panel-label" style="margin-top:18px;">Or try one of these</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(EXAMPLES))
    for c, (label, text) in zip(chip_cols, EXAMPLES.items()):
        with c:
            st.button(label, on_click=set_example, args=(text,), use_container_width=True)

    st.write("")
    scan_clicked = st.button("Scan Message", type="primary", use_container_width=True)
    if scan_clicked:
        if st.session_state.message_text.strip():
            st.session_state.result = run_prediction(st.session_state.message_text)
        else:
            st.session_state.result = None

with col_result:
    st.markdown('<div class="panel-label">Verdict</div>', unsafe_allow_html=True)
    result = st.session_state.result

    if result is None:
        st.markdown(
            """
            <div class="verdict idle">
                <div class="verdict-label">— AWAITING INPUT —</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        is_spam = result["final"] == 1
        agree = sum(1 for v in result["sub"].values() if v == result["final"])
        verdict_class = "spam" if is_spam else "ham"
        verdict_text = "SPAM" if is_spam else "NOT SPAM"

        st.markdown(
            f"""
            <div class="verdict {verdict_class}">
                <div class="verdict-label">{verdict_text}</div>
                <div class="verdict-sub">{agree} / 3 MODELS AGREE</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sensor_html = '<div class="sensor-row">'
        for key, label in MODEL_NAMES.items():
            vote = result["sub"][key]
            cls = "spam" if vote == 1 else "ham"
            vote_text = "SPAM" if vote == 1 else "HAM"
            sensor_html += (
                f'<div class="sensor {cls}"><span class="sensor-dot"></span>'
                f'<span class="sensor-label">{html.escape(label.upper())}</span>'
                f'<span class="sensor-verdict">{vote_text}</span></div>'
            )
        sensor_html += "</div>"
        st.markdown(sensor_html, unsafe_allow_html=True)

        if result["spam_terms"] or result["ham_terms"]:
            st.markdown('<div class="panel-label">Signal terms in this message</div>', unsafe_allow_html=True)
            chips = ""
            for term in result["spam_terms"]:
                chips += f'<span class="term-chip spam">{html.escape(term)}</span>'
            for term in result["ham_terms"]:
                chips += f'<span class="term-chip ham">{html.escape(term)}</span>'
            st.markdown(chips, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="footnote">
    <b>How it works</b> — a logistic regression, a multinomial naive Bayes, and a linear SVM each vote
    independently on TF-IDF features (unigrams + bigrams) of the message. The majority vote wins.
    Vocabulary: <b>{vocab_size:,}</b> terms, learned from the training set.
    </div>
    """,
    unsafe_allow_html=True,
)
