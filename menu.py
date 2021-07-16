import streamlit as st

import archive
import test

st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Please select a page", ["RealTime",
                                                         "Archive"])

if app_mode == "RealTime":
    test.load_page()
elif app_mode == "Archive":
    archive.load_page()
