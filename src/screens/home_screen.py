import streamlit as st
from pathlib import Path

from src.screens.components.header import header_home
from src.screens.ui.base_layout import style_base_layout, style_background_home


def home_screen():
    style_background_home()
    style_base_layout()
    header_home()

    # Asset paths for illustrations
    project_root = Path(__file__).resolve().parents[2]
    student_img = project_root / "assets" / "student_illustration.png"
    teacher_img = project_root / "assets" / "teacher_illustration.png"

    # Side-by-side equal dimension portal cards
    col1, col2 = st.columns(2, gap="large")

    with col1:
        with st.container(border=True):
            if student_img.exists():
                st.image(str(student_img), use_container_width=True)
            if st.button("Student Portal", key="btn_student_portal", use_container_width=True):
                st.session_state["login_type"] = "student"
                st.rerun()

    with col2:
        with st.container(border=True):
            if teacher_img.exists():
                st.image(str(teacher_img), use_container_width=True)
            if st.button("Teacher Portal", key="btn_teacher_portal", use_container_width=True):
                st.session_state["login_type"] = "teacher"
                st.rerun()