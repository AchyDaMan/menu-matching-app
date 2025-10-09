import streamlit as st
import joblib
import pandas as pd

# --------------------------
# Load your .joblib file
# --------------------------
@st.cache_resource
def load_data(joblib_path):
    try:
        dataframes = joblib.load(joblib_path)
        # Ensure it's a list and each has a .name attribute
        for i, df in enumerate(dataframes):
            df.name = df.attrs.get("name", f"DataFrame_{i+1}")
        return dataframes
    except Exception as e:
        st.error(f"Error loading joblib file: {e}")
        return []


# --------------------------
# Streamlit UI
# --------------------------
st.set_page_config(page_title="Results Viewer", layout="wide")

st.title("View Data here")

# Sidebar for file input
st.sidebar.header("Load Data")

import os

# Try auto-loading first
joblib_files = [f for f in os.listdir() if f.endswith(".joblib")]

joblib_file = None
if joblib_files:
    st.sidebar.success(f"Auto-loaded file: {joblib_files[0]}")
    joblib_file = joblib_files[0]
else:
    # Fall back to upload
    st.sidebar.info("No .joblib file found in the current directory.")
    joblib_file = st.sidebar.file_uploader("Or upload your .joblib file", type=["joblib"])

if joblib_file:
    dataframes = load_data(joblib_file)
else:
    st.stop()


if dataframes:
    # Search box
    search_query = st.sidebar.text_input("🔍 Search DataFrames by name", "").strip().lower()

    # Filtered list of dataframe names
    filtered_dfs = [df for df in dataframes if search_query in df.name.lower()]

    if not filtered_dfs:
        st.sidebar.warning("No matching DataFrames found.")
    else:
        # Dropdown to select DataFrame
        selected_name = st.sidebar.radio(
            "Select a DataFrame:",
            options=[df.name for df in filtered_dfs],
            index=0,
        )

        # Find selected df
        selected_df = next(df for df in dataframes if df.name == selected_name)

        # Display selected DataFrame
        st.subheader(f"📄 {selected_df.name}")
        st.write(f"Shape: {selected_df.shape[0]} rows × {selected_df.shape[1]} columns")
        st.dataframe(selected_df)
else:
    st.info("👈 Upload a `.joblib` file to begin.")


