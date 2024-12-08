# List of imports
import streamlit as st
import pandas as pd
import numpy as np

import utils.data_processing_helpers as dp

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
save_cont = st.container()


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
        df_trans = df.copy()
        st.success('Data imported!', icon="✅")
        st.divider()

        # Transform your data
        with format_cont:
            st.markdown('<h4>Transform your data</h4>',unsafe_allow_html=True)

            with st.expander('Select the desired format for your variables.', expanded=False):
                format_vars = pd.DataFrame({"Variable": df_trans.columns,"Type": df_trans.dtypes})
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
                
                if st.button("Change formats"):
                    for type in list(format_vars['Type'].unique()):
                        for col in list(format_vars.loc[format_vars['Type']==type,"Variable"].unique()):
                            if type == "int64":
                                df_trans[col] = df_trans[col].astype(int)
                            elif type == "float64":
                                df_trans[col] = pd.to_numeric(df_trans[col], errors='coerce')
                            elif type == "object":
                                df_trans[col] = df_trans[col].astype(str)
                            elif type == "datetime64":
                                df_trans[col] = pd.to_datetime(df_trans[col], format="%Y-%m-%d", errors='coerce')
                    st.success(f"Formats changed!", icon="✅")
            
            with st.expander('Imput missing values.', expanded=False):
                missing_vars = dp.plot_missing_values(df_trans)
                col_for_missing = st.selectbox("Select a column to fill missing values", missing_vars)
                fill_method = st.selectbox("Fill method", ["Mean", "Median", "Mode", "Custom Value"])

                if st.button("Fill Missing Values"):
                    if fill_method == "Mean":
                        df_trans[col_for_missing].fillna(df_trans[col_for_missing].mean(), inplace=True)
                    elif fill_method == "Median":
                        df_trans[col_for_missing].fillna(df_trans[col_for_missing].median(), inplace=True)
                    elif fill_method == "Mode":
                        df_trans[col_for_missing].fillna(df_trans[col_for_missing].mode()[0], inplace=True)
                    elif fill_method == "Custom Value":
                        custom_value = st.text_input("Custom value")
                        if custom_value:
                            df_trans[col_for_missing].fillna(custom_value, inplace=True)
                    st.success(f"Missing values filled in column '{col_for_missing}' using {fill_method}!", icon="✅")

            with st.expander('Remove outliers.', expanded=False):
                col_for_outliers = st.selectbox("Select a column to remove outliers", df_trans.select_dtypes(include=[np.number]).columns)
                threshold = st.slider("Outlier threshold (z-score)", 1.0, 5.0, 3.0)
                
                if st.button("Remove Outliers"):
                    from scipy.stats import zscore
                    z_scores = zscore(df_trans[col_for_outliers].dropna())
                    df_trans = df_trans[(np.abs(z_scores) < threshold) | df_trans[col_for_outliers].isna()]
                    st.success(f"Outliers removed from column '{col_for_outliers}' (z-score threshold: {threshold})!", icon="✅")
            
            # Compare datasets
            col1, col2 = st.columns(2)
            col1.text("Old dataset")
            col1.dataframe(df,hide_index=True)
            col2.text("Cleaned dataset")
            col2.dataframe(df_trans,hide_index=True)
            st.divider()

        # Save your data
        with save_cont:
            st.markdown('<h4>Save your data</h4>',unsafe_allow_html=True)
            csv = dp.convert_df(df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name="large_df.csv",
                mime="text/csv",
            )