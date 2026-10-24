import streamlit as st
import time
from src.database.db import get_subject_by_code, is_student_enrolled, enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']

    clean_code = subject_code.strip() if subject_code else ""
    subject = get_subject_by_code(clean_code)
    if not subject:
        st.error(f"Subject code '{clean_code}' not found!")
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return

    if is_student_enrolled(student_id, subject['subject_id']):
        st.info("You're already enrolled in this course!")
        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject.get('name', clean_code)}**?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch'):
            res = enroll_student_to_subject(student_id, subject['subject_id'])
            if res:
                st.success('Joined successfully!')
            else:
                st.error('Enrollment failed.')
            st.query_params.clear()
            time.sleep(1.5)
            st.rerun()
