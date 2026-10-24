import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "snapclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.image(out.getvalue(), width=200)

    with col2:
        st.write(f"Scan this QR or use this link to enroll in **{subject_name}**")
        st.code(join_url, language="text")
        st.markdown(f"**Subject Code:** `{subject_code}`")