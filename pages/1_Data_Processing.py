# List of imports
import streamlit as st
import pandas as pd
import numpy as np



#-------------------------------------------------------------------------------
# App settings

st.set_page_config(
    page_title="The Analyzer",
    #page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------------
# Data Processing page

title_cont = st.container()
intro_cont = st.container()
import_cont = st.container()
format_cont = st.container()


# Title
with title_cont:
    col1, col2, col3 = st.columns([1,5,1], gap="small")
    col2.markdown("<p><span style='font-size:60px;'>The </span><span style='font-weight:bolder;font-size:60px;'> Analyzer</span></p>",unsafe_allow_html=True)
    st.title('Data Processing')
    st.write('')

# Introduction
with intro_cont:
    st.markdown(
        """
        The Data Processing tool will allow you to import and clean your dataset.\n
        You will be able to change the format of your columns, remove outliers, fill missing values...
        """
    )
    st.divider()

# Import your data
with import_cont:
    st.markdown('<h4>Import your data</h4>',unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file:
        # Read the uploaded file
        df = pd.read_csv(uploaded_file)
        st.success('Data imported!', icon="✅")
        st.dataframe(df,hide_index=True)
        st.divider()

        # Transform your data
        with format_cont:
            st.markdown('<h4>Transform your data</h4>',unsafe_allow_html=True)

            st.text('Select the desired format for your variables.')
            format_vars = pd.DataFrame({"Variable": df.columns,"Type": df.dtypes})
            format_vars["Type"] = format_vars["Type"].astype("str")
            format_vars = st.data_editor(format_vars,
                            column_config={
                                    "Type": st.column_config.SelectboxColumn(
                                    "Type",
                                    help="The type of the variable",
                                    width="small",
                                    options=["int64","float64","object","datetime64"],
                                    required=True
                                )
                            },use_container_width=False,hide_index=True)
            
            for type in list(format_vars['Type'].unique()):
                for col in list(format_vars.loc[format_vars['Type']==type,"Variable"].unique()):
                    if type == "int64":
                        df[col] = df[col].astype(int)
                    elif type == "float64":
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif type == "object":
                        df[col] = df[col].astype(str)
                    elif type == "datetime64":
                        df[col] = pd.to_datetime(df[col], format="%Y-%m-%d", errors='coerce')
            st.dataframe(df,hide_index=True)



            st.divider()