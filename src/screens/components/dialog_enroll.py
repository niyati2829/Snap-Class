import streamlit as st
import time
from src.database.db import get_subject_by_code, is_student_enrolled, enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='e.g. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        clean_code = join_code.strip() if join_code else ""
        if clean_code:
            subject = get_subject_by_code(clean_code)
            if subject:
                student_id = st.session_state.student_data['student_id']

                if is_student_enrolled(student_id, subject['subject_id']):
                    st.warning('You are already enrolled in this course!')
                else:
                    res = enroll_student_to_subject(student_id, subject['subject_id'])
                    if res:
                        st.success(f"Successfully enrolled in {subject.get('name', clean_code)}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Enrollment failed. Please try again.")
            else:
                st.warning(f"Subject with code '{clean_code}' not found. Please check with your teacher.")
        else:
            st.warning('Please enter a subject code')
