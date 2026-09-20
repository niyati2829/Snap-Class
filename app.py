import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen

if "login_type" not in st.session_state:
    st.session_state["login_type"] = None

if st.session_state["login_type"] == "teacher":
    teacher_screen()
elif st.session_state["login_type"] == "student":
    student_screen()
else:
    home_screen()
