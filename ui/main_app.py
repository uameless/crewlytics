import streamlit as st
import os
import tempfile
from ui import components
from ui.state_manager import init_session_state
from workflows.analysis_workflow import build_analysis_graph

def main():
    # Setup Streamlit page
    st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")
    st.title("📊 AI-Powered Product Data Analyzer")
    st.markdown("Upload your dataset and let the AI crew clean, analyze, visualize, and summarize your data.")

    # Initialize session state
    init_session_state()

    # Upload dataset
    uploaded_file = components.dataset_uploader()

    # Get user instruction
    user_instruction = components.instruction_input()

    # If file uploaded, store in temp directory
    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["file_path"] = file_path
        st.session_state["user_instruction"] = user_instruction

    # Run analysis
    if uploaded_file and st.button("Run AI Analysis 🚀"):
        st.info("⏳ Running AI multi-agent pipeline... please wait.")
        graph = build_analysis_graph()
        final_state = graph.invoke({
            "file_path": st.session_state["file_path"],
            "user_instruction": st.session_state["user_instruction"]
        })

        # Store results in session state
        st.session_state["df_cleaned"] = final_state["df_cleaned"]
        st.session_state["chart_paths"] = final_state["chart_paths"]
        st.session_state["insight_text"] = final_state["insight_text"]
        st.session_state["report_file"] = final_state["report_file"]


        st.success("✅ Analysis complete!")

    # Display results if analysis has been run
    if st.session_state["df_cleaned"] is not None:
        components.show_dataset_preview(st.session_state["df_cleaned"])

    if st.session_state["chart_paths"]:
        components.show_charts(st.session_state["chart_paths"])

    if st.session_state["insight_text"]:
        components.show_insights(st.session_state["insight_text"])

    if st.session_state["report_file"]:
        components.show_report_download(st.session_state["report_file"])

    st.markdown("---")
    st.caption("AI Multi-Agent Data Analysis System")

if __name__ == "__main__":
    main()
