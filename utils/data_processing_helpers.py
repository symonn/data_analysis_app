# List of imports
import streamlit as st
import pandas as pd
import numpy as np


def plot_missing_values(df):

    # Calculate missing value percentages
    missing_percentage = df.isnull().mean() * 100
    missing_percentage = missing_percentage[missing_percentage > 0]
    if not missing_percentage.empty:
        st.bar_chart(missing_percentage,y_label="Percentage (%)")
        return list(missing_percentage.index)
    else:
        st.write("No missing values in the dataset.")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")