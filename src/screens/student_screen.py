import streamlit as st
import numpy as np
import time
from PIL import Image

from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button("Logout", type='secondary', key='studentlogoutbtn'):
            st.session_state['is_logged_in'] = False
            if 'student_data' in st.session_state:
                del st.session_state.student_data
            st.rerun()

    st.space()

    col1, col2 = st.columns(2)
    with col1:
        st.header('Enrolled Subjects')
    with col2:
        if st.button('Enroll into a new subject', width='stretch', icon=':material/add_circle:'):
            enroll_dialog()

    # List all enrolled subjects
    subjects = get_student_subjects(student_id)
    if not subjects:
        st.info("You haven't enrolled in any subjects yet! Use the button above to enroll.")
        footer_dashboard()
        return

    logs = get_student_attendance(student_id)
    stats_map = {}
    for log in logs:
        sid = log.get('subject_id')
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node.get('subjects', {})
        sid = sub.get('subject_id')

        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        def make_unenroll_button(s_id=sid, s_name=sub.get('name', 'Course')):
            def unenroll_button():
                if st.button("Unenroll from this course", key=f"unenroll_{s_id}", type='tertiary', width='stretch', icon=':material/delete_forever:'):
                    unenroll_student_to_subject(student_id, s_id)
                    st.toast(f"Unenrolled from {s_name} successfully!")
                    st.rerun()
            return unenroll_button

        with cols[i % 2]:
            subject_card(
                name=sub.get('name', 'Untitled Subject'),
                code=sub.get('subject_code', 'N/A'),
                section=sub.get('section', '-'),
                stats=[
                    ('📅', 'Classes Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=make_unenroll_button(sid, sub.get('name', 'Course'))
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

    c1, c2 = st.columns([3, 1], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn'):
            st.session_state['login_type'] = None
            st.rerun()

    st.markdown("<h2 style='text-align: center; margin-bottom: 8px;'>Student FaceID Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b; margin-bottom: 24px;'>Position your face in the camera to log in or register a new student account</p>", unsafe_allow_html=True)

    # Centered container for camera and registration
    _, col_center, _ = st.columns([1, 2.5, 1])

    with col_center:
        photo_source = st.camera_input("Take a snapshot", label_visibility="collapsed")

        if 'show_manual_register' not in st.session_state:
            st.session_state['show_manual_register'] = False

        show_registration = st.session_state['show_manual_register']

        if photo_source:
            img = np.array(Image.open(photo_source))

            with st.spinner('Scanning face...'):
                detected, all_ids, num_faces = predict_attendance(img)

                if num_faces == 0:
                    st.warning('No face detected in the snapshot. Please look directly at the camera.')
                elif num_faces > 1:
                    st.warning('Multiple faces detected. Please ensure only one person is in the frame.')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        all_students = get_all_students()
                        student = next((s for s in all_students if str(s.get('student_id')) == str(student_id)), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.toast(f"Welcome Back, {student.get('name', 'Student')}!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info('Face not recognized in registered student records. Register your new profile below!')
                        show_registration = True

        st.space()

        # Registration Form
        if show_registration or photo_source:
            with st.container(border=True):
                st.markdown("<h3 style='margin-top:0;'>Register New Student Profile</h3>", unsafe_allow_html=True)
                new_name = st.text_input("Full Name", placeholder="e.g. Ananya Sharma")

                st.subheader("Optional: Voice Enrollment")
                st.caption("Enroll your voice to enable hands-free voice-based attendance recording.")

                audio_data = None
                try:
                    audio_data = st.audio_input("Record phrase: 'I am present'")
                except Exception as e:
                    st.warning(f"Audio device notice: {e}")

                if st.button("Create Student Account", type='primary', width='stretch'):
                    if not new_name.strip():
                        st.warning("Please enter your name!")
                    elif not photo_source:
                        st.warning("Please take a photo with the camera above so your face can be enrolled!")
                    else:
                        with st.spinner("Creating your student profile..."):
                            # 1. Process face embedding
                            img = np.array(Image.open(photo_source))
                            encodings = get_face_embeddings(img)
                            if not encodings:
                                st.error("Could not extract facial features. Please retake a clear, well-lit photo.")
                            else:
                                face_emb = encodings[0].tolist()

                                # 2. Process voice embedding (optional)
                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(audio_data)

                                # 3. Save student account
                                response_data = create_student(
                                    new_name.strip(),
                                    face_embedding=face_emb,
                                    voice_embedding=voice_emb
                                )

                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]
                                    st.toast(f"Profile Created! Welcome, {new_name.strip()}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error("Could not save account. Please try again.")

    footer_dashboard()