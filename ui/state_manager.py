import streamlit as st

def init_session_state():
    defaults = {
        "file_path": None,
        "user_instruction": "",
        "df_cleaned": None,
        "chart_paths": [],
        "insight_text": "",
        "report_file": ""
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
