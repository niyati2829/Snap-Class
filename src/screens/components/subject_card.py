import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    stats_html = ""
    if stats:
        badges = "".join([
            f'<div style="background: rgba(235, 69, 158, 0.08); color: #1e293b; padding: 6px 12px; border-radius: 12px; font-size: 0.88rem; font-weight: 500; display: inline-flex; align-items: center; gap: 6px;">{icon} <b>{value}</b> {label}</div>'
            for icon, label, value in stats
        ])
        stats_html = f'<div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; margin-bottom: 8px;">{badges}</div>'

    card_html = (
        f'<div style="background: white; border-left: 8px solid #EB459E; padding: 22px; border-radius: 18px; box-shadow: 0 4px 14px rgba(0,0,0,0.06); margin-bottom: 16px;">'
        f'<h3 style="margin: 0; color: #1e293b; font-size: 1.4rem; font-weight: 700;">{name}</h3>'
        f'<p style="color: #64748b; margin: 8px 0 14px 0; font-size: 0.95rem;">'
        f'Code: <span style="background: #E0E3FF; color: #5865F2; padding: 3px 8px; border-radius: 6px; font-weight: 600;">{code}</span> '
        f'&nbsp;|&nbsp; Section: <b>{section}</b>'
        f'</p>'
        f'{stats_html}'
        f'</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()