import streamlit as st
import pandas as pd

from src.scam_analyzer import analyze_message
from src.react_agent import analyze_with_tools
from src.feedback_manager import save_feedback


st.set_page_config(
    page_title="ScamGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.sidebar.title("🛡️ ScamGuard AI")
st.sidebar.markdown("""
### Features
✅ Scam Detection  
✅ Intent Detection  
✅ Risk Scoring  
✅ Gemini LLM  
✅ Prompt Engineering  
✅ ReAct Tool Workflow  
✅ URL Safety Analysis  
✅ Threat Intelligence  
✅ Multilingual Detection  
✅ Feedback Loop  
""")

st.title("🛡️ ScamGuard AI")
st.markdown(
    "Protecting users from scam messages using Generative AI, threat intelligence, and explainable risk analysis."
)

message = st.text_area(
    "Enter a message to analyze",
    height=150,
    placeholder="Example: Your SBI account will be blocked. Verify KYC immediately at http://sbi-verify-now.com"
)

mode = st.selectbox(
    "Select Analysis Mode",
    ["zero_shot", "few_shot", "cot", "react"],
    index=3
)

analyze_button = st.button("Analyze Message", type="primary")


def show_risk_status(score: int):
    st.progress(score / 100)

    if score >= 80:
        st.error("🚨 High Risk")
    elif score >= 50:
        st.warning("⚠️ Medium Risk")
    else:
        st.success("✅ Low Risk")


if analyze_button:

    if not message.strip():
        st.warning("Please enter a message.")
        st.stop()

    try:
        with st.spinner("Analyzing message..."):

            if mode == "react":
                result = analyze_with_tools(message)

                classification = result["classification"]
                intent_type = result["intent_type"]
                risk_score = result["final_risk_score"]
                reason = result["reason"]
                safe_action = result["safe_action"]

                st.success("Analysis Complete")

                col1, col2, col3 = st.columns(3)

                col1.metric("Classification", classification)
                col2.metric("Intent Type", intent_type)
                col3.metric("Risk Score", f"{risk_score}/100")

                show_risk_status(risk_score)

                st.subheader("Reason")
                st.write(reason)

                st.subheader("Recommended Safe Action")
                st.write(safe_action)

                st.subheader("Language Detection")
                st.info(result.get("detected_language", "Unknown"))

                st.subheader("Threat Intelligence")

                if result.get("known_scam_pattern"):
                    st.error("Known scam message pattern detected.")
                else:
                    st.success("No known scam message pattern detected.")

                keyword_matches = result.get("threat_keyword_matches", [])

                if keyword_matches:
                    st.write("Matched scam keywords:")
                    st.write(keyword_matches)

                st.subheader("URL Analysis")

                url_analysis = result.get("url_analysis", [])

                if url_analysis:
                    url_df = pd.DataFrame(url_analysis)
                    st.dataframe(url_df, use_container_width=True)
                    st.write(result.get("url_summary", ""))
                else:
                    st.info("No URLs found in the message.")

            else:
                result = analyze_message(message, mode=mode)

                classification = result.classification
                intent_type = result.intent_type
                risk_score = result.risk_score
                reason = result.reason
                safe_action = result.safe_action

                st.success("Analysis Complete")

                col1, col2, col3 = st.columns(3)

                col1.metric("Classification", classification)
                col2.metric("Intent Type", intent_type)
                col3.metric("Risk Score", f"{risk_score}/100")

                show_risk_status(risk_score)

                st.subheader("Reason")
                st.write(reason)

                st.subheader("Recommended Safe Action")
                st.write(safe_action)

            st.divider()

            st.subheader("Feedback")

            feedback = st.radio(
                "Was this prediction correct?",
                ["Yes", "No"],
                horizontal=True
            )

            correct_label = ""
            correct_intent = ""

            if feedback == "No":
                correct_label = st.selectbox(
                    "Correct Classification",
                    ["Scam", "Not Scam", "Uncertain"]
                )

                correct_intent = st.text_input(
                    "Correct Intent Type"
                )

            if st.button("Submit Feedback"):
                save_feedback(
                    message=message,
                    predicted_label=classification,
                    predicted_intent=intent_type,
                    user_feedback=feedback,
                    correct_label=correct_label,
                    correct_intent=correct_intent,
                )

                st.success("Feedback saved successfully.")

    except Exception as e:
        st.error("Something went wrong during analysis.")
        st.exception(e)