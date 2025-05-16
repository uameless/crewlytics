import streamlit as st
import pandas as pd

def dataset_uploader():
    return st.file_uploader(
        "Upload your dataset (.csv, .xlsx, .json)",
        type=["csv", "xlsx", "json"]
    )

def instruction_input():
    return st.text_input(
        "Optional: What do you want the AI to focus on? (e.g., 'Find sales trends')"
    )

def show_dataset_preview(df: pd.DataFrame):
    st.subheader("📄 Cleaned Dataset Preview")
    st.dataframe(df.head())

def show_charts(chart_paths: list):
    st.subheader("📈 Visual Reports")
    for chart_file in chart_paths:
        st.image(chart_file, use_column_width=True)

def show_insights(summary_text: str):
    st.subheader("📝 AI-Generated Insight Summary")
    st.text_area("Insights", summary_text, height=300)

def show_report_download(report_path: str):
    st.subheader("📥 Download Full Report")
    with open(report_path, "rb") as file:
        st.download_button(
            label="Download Analysis Report (HTML)",
            data=file,
            file_name="AI_Analysis_Report.html",
            mime="text/html"
        )
