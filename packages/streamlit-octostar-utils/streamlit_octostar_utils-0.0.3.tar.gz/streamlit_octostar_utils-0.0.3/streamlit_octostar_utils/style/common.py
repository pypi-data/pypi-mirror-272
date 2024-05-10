import streamlit as st

def hide_streamlit_header():
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
    hide_streamlit_top = """
    <style>
        #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    </style>
    """
    st.markdown(hide_streamlit_top, unsafe_allow_html=True)
    hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)