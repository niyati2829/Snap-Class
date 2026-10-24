import streamlit as st

def footer_home():
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 1rem 0; color: #5865F2; opacity: 0.85; font-size: 0.9rem; font-family: 'Outfit', 'Montserrat', sans-serif; font-weight: 600;">
            SnapClass &bull; AI-Powered Attendance Management
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer_dashboard():
    st.markdown(
        """
        <div style="text-align: center; padding: 2.5rem 0 1rem 0; color: #5865F2; opacity: 0.85; font-size: 0.9rem; font-family: 'Outfit', 'Montserrat', sans-serif; font-weight: 600;">
            SnapClass &bull; AI Smart Attendance Management
        </div>
        """,
        unsafe_allow_html=True,
    )
