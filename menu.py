import streamlit as st
import archive
import realtime
import stats

st.set_page_config(
    page_title="Помощник журналиста",
    layout="wide")

st.sidebar.title("Меню")
app_mode = st.sidebar.selectbox("Выберите страницу", ["Помощник журналиста", "Архив статей", "Статистика"])

if app_mode == "Помощник журналиста":
    realtime.load_page()
elif app_mode == "Архив статей":
    archive.load_page()
elif app_mode == "Статистика":
    stats.load_page()
