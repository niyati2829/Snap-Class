import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject:")
    sub_code = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")

    if st.button("Create Subject Now", type='primary', width='stretch'):
        if sub_code and sub_name and sub_section:
            try:
                res = create_subject(sub_code, sub_name, sub_section, teacher_id)
                if res is not None:
                    st.toast("Subject Created Successfully!")
                    st.rerun()
                else:
                    st.error("Failed to create subject. Please check database connection.")
            except Exception as e:
                st.error(f"Error creating subject: {e}")
        else:
            st.warning("Please fill all the fields")
