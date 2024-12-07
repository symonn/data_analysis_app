# List of imports
import streamlit as st
import pandas as pd
import numpy as np


def main():

    #-------------------------------------------------------------------------------
    # App settings

    st.set_page_config(
        page_title="The Analyzer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # -------------------------------------------------------------------------------
    # Home page

    title_cont = st.container()
    intro_cont = st.container()
    side_cont = st.sidebar

    with title_cont:
        title_col1, title_col2, title_col3 = st.columns([1,5,1], gap="small")
        title_col2.markdown("<p><span style='font-size:60px;'>The </span><span style='font-weight:bolder;font-size:60px;'>Analyzer</span></p>",unsafe_allow_html=True)

    with intro_cont:
        # Home Page
        st.title('Home Page')

        st.markdown('The Analyzer Portal will contain different tools to help you to process your data and use ML to find insights in your dataset.\n')
        st.write('')

    with side_cont:
            # Sidebar
            st.sidebar.title(f'Welcome')

if __name__ == "__main__":
    main()
