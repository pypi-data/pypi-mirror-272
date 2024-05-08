import streamlit as st

def hide_icons():
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>"""
    st.markdown(hide_st_style, unsafe_allow_html=True)


def hide_sidebar():
    no_sidebar_style = """
                <style>
                div[data-testid="stSidebarNav"] {visibility: hidden;}
                </style>"""
    st.markdown(no_sidebar_style, unsafe_allow_html=True)


def remove_whitespaces():
    st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
