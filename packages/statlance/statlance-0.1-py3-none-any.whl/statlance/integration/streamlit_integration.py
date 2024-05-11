# statlance/integration/streamlit_integration.py
import streamlit as st
from statlance.core.dashboarding import main as streamlit_main

def run_streamlit_app():
    st.set_page_config(layout="wide")
    streamlit_main()

