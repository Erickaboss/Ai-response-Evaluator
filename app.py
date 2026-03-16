"""
app.py
Streamlit browser UI for the AI Response Evaluator.
Run with: python -m streamlit run app.py
"""

import streamlit as st
from evaluator import (
    score_clarity,
    score_completeness,
    score_reasoning,
    score_examples,
    score_length_readability,
)
from feedback import compute_final_score, CRITERIA_WEIGHTS
from examples import EXAMPLES

st.set_page_config(page_title="AI Response Evaluator", page_icon="🤖", layout="centered")

st.title("🤖 AI Response Evaluator")
st.caption("Simulate the work of an AI training engineer — score and critique model responses.")

# --- Sidebar: load examples ---
st.sidebar.header("Quick Load Examples")
if st.sidebar.button("Load Example 1 (Strong response)"):
    st.session_state["prompt"] = EXAMPLES[0]["prompt"]
    st.session_state["response"] = EXAMPLES[0]["response"]
if st.sidebar.button("Load Example 2 (Weak response)"):
    st.session_state["prompt"] = EXAMPLES[1]["prompt"]
    st.session_state["response"] = EXAMPLES[1]["response"]

st.sidebar.markdown("---")
st.sidebar.markdown("**Criteria weights**")
for criterion, weight in CRITERIA_WEIGHTS.items():
    st.sidebar.markdown(f"- {criterion}: `{int(weight*100)}%`")

# --- Main inputs ---
prompt = st.text_area(
    "User Prompt",
    value=st.session_state.get("prompt", ""),
    placeholder="e.g. Explain what a Python decorator is and how to use it.",
    height=100,
)

response = st.text_area(
    "Model Response",
    value=st.session_state.get("response", ""),
    placeholder="Paste the AI-generated response here...",
    height=200,
)

evaluate_btn = st.button("Evaluate", type="primary", use_container_width=True)

# --- Evaluation ---
if evaluate_btn:
    if not prompt.strip() or not response.strip():
        st.warning("Please fill in both the prompt and the response.")
    else:
        results = {
            "Clarity":              score_clarity(response),
            "Completeness":         score_completeness(prompt, response),
            "Reasoning":            score_reasoning(response),
            "Example Usage":        score_examples(response),
            "Length & Readability": score_length_readability(response),
        }
        scores     = {k: v[0] for k, v in results.items()}
        rationales = {k: v[1] for k, v in results.items()}
        final      = compute_final_score(scores)

        # Final score banner
        if final >= 8.5:
            verdict, color = "Excellent response", "green"
        elif final >= 7.0:
            verdict, color = "Good — minor room for improvement", "blue"
        elif final >= 5.0:
            verdict, color = "Acceptable — notable gaps exist", "orange"
        else:
            verdict, color = "Poor — significant improvements needed", "red"

        st.markdown("---")
        st.subheader("Evaluation Results")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Final Score", f"{final} / 10")
        with col2:
            st.markdown(f"**Verdict:** :{color}[{verdict}]")

        st.markdown("---")

        # Per-criterion breakdown
        for criterion in CRITERIA_WEIGHTS:
            score     = scores[criterion]
            rationale = rationales[criterion]
            weight    = int(CRITERIA_WEIGHTS[criterion] * 100)

            with st.expander(f"{criterion}  —  {score}/10  (weight: {weight}%)"):
                st.progress(score / 10)
                st.write(rationale)
