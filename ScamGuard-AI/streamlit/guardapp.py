import streamlit as st
import pandas as pd

from src.scam_analyzer import analyze_message
from src.react_agent import analyze_with_tools
from src.feedback_manager import save_feedback
from evaluation.evaluate import evaluate_dataframe


st.set_page_config(
    page_title="ScamGuard AI",
    page_icon="🛡️",
    layout="wide"
)
st.error("NEW DATASET EVALUATION VERSION LOADED")
st.sidebar.title("🛡️ ScamGuard AI")

st.sidebar.header("Navigation")

app_mode = st.sidebar.selectbox(
    "Choose what you want to do",
    ["Analyze Message", "Evaluate Dataset"]
)

st.sidebar.write("Current Mode:", app_mode)

st.sidebar.markdown("""
### Features
✅ Scam Detection  
✅ Intent Detection  
✅ Risk Scoring  
✅ Prompt Engineering  
✅ ReAct Tool Workflow  
✅ URL Safety Analysis  
✅ Threat Intelligence  
✅ Multilingual Detection  
✅ Feedback Loop  
✅ Dataset Evaluation  
""")


def show_risk_status(score: int):
    st.progress(score / 100)

    if score >= 80:
        st.error("🚨 High Risk")
    elif score >= 50:
        st.warning("⚠️ Medium Risk")
    else:
        st.success("✅ Low Risk")


st.title("🛡️ ScamGuard AI")
st.markdown(
    "Protecting users from scam messages using Gemini, prompt engineering, threat intelligence, and explainable risk analysis."
)


if app_mode == "Analyze Message":

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

    if st.button("Analyze Message", type="primary"):

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
                        #st.dataframe(url_df, use_container_width=True)
                        st.dataframe(url_df.head(), width="stretch")
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


elif app_mode == "Evaluate Dataset":

    st.header("📊 Dataset Evaluation")

    st.markdown("""
    Upload a CSV dataset with these required columns:

    - `message_text`
    - `label`
    - `intent_type`
    """)

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"]
    )

    eval_mode = st.selectbox(
        "Select Prompt Mode",
        ["zero_shot", "few_shot", "cot", "react"],
        index=1
    )

    sample_size = st.number_input(
        "Sample Size",
        min_value=1,
        value=20,
        step=1
    )

    run_eval = st.button(
        "Run Dataset Evaluation",
        type="primary"
    )

    if run_eval:

        if uploaded_file is None:
            st.warning("Please upload a dataset.")
            st.stop()

        try:
            df = pd.read_csv(uploaded_file)

            st.subheader("Dataset Preview")
            st.dataframe(df.head(), use_container_width=True)

            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_callback(current, total):
                progress_bar.progress(current / total)
                status_text.write(f"Processed {current}/{total}")

            with st.spinner("Evaluating dataset..."):

                results = evaluate_dataframe(
                    df=df,
                    mode=eval_mode,
                    sample_size=sample_size,
                    sleep_time=0,
                    progress_callback=progress_callback,
                )

            st.success("Evaluation Complete")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Accuracy",
                f"{results['label_accuracy']:.4f}"
            )

            col2.metric(
                "Precision",
                f"{results['precision']:.4f}"
            )

            col3.metric(
                "Recall",
                f"{results['recall']:.4f}"
            )

            col4.metric(
                "F1 Score",
                f"{results['f1_score']:.4f}"
            )

            col5, col6, col7 = st.columns(3)

            col5.metric(
                "Intent Accuracy",
                f"{results['intent_accuracy']:.4f}"
            )

            col6.metric(
                "Valid Samples",
                results["valid_samples"]
            )

            col7.metric(
                "Errors",
                results["errors"]
            )

            st.subheader("Confusion Matrix")
            st.write(results["confusion_matrix"])

            st.subheader("Prediction Results")
            st.dataframe(
                results["results_df"],
                use_container_width=True
            )

            csv_data = (
                results["results_df"]
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="Download Results CSV",
                data=csv_data,
                file_name=f"results_{eval_mode}.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error("Dataset evaluation failed.")
            st.exception(e)