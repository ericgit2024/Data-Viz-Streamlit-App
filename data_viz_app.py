import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import StringIO, BytesIO

# Set up page configuration
st.set_page_config(page_title="DataViz - Interactive Data Exploration and Visualization tool", layout="wide")

# App Title
st.title("DataViz - Interactive Data Exploration and Visualization Tool")

# Centered file uploader
st.subheader("Upload Your Data")
file = st.file_uploader("Upload your CSV, Excel file", type=["csv", "xlsx", "xls"])

# Load data
if file is not None:
    if file.name.endswith(".csv"):
        data = pd.read_csv(file)
    elif file.name.endswith((".xlsx", ".xls")):
        data = pd.read_excel(file)
    
    # Display data
    st.write("### Loaded Data", data.head())
else:
    st.info("Please upload a CSV/Excel file to proceed.")

# Data Processing
if file is not None:
    st.sidebar.subheader("Data Processing Options")

    # Column selection
    columns = st.sidebar.multiselect("Select columns for analysis", options=data.columns, default=data.columns)

    # Missing value handling
    if st.sidebar.checkbox("Handle missing values"):
        method = st.sidebar.selectbox("Choose method", ["Drop missing values", "Fill missing values"])
        if method == "Drop missing values":
            data = data.dropna()
        elif method == "Fill missing values":
            fill_value = st.sidebar.text_input("Enter fill value", "0")
            data = data.fillna(fill_value)
    
    # Convert data types
    if st.sidebar.checkbox("Convert Data Types"):
        for col in columns:
            if data[col].dtype == "object":
                data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0)

    # Remove special characters
    if st.sidebar.checkbox("Remove special characters from string columns"):
        for col in data.select_dtypes(include="object").columns:
            data[col] = data[col].str.replace(r'[^\w\s]', '', regex=True)
    
    st.write("### Processed Data", data[columns].head())

# Data Visualization
if file is not None:
    # Univariate Analysis
    st.subheader("Univariate Analysis")
    univariate_col = st.selectbox("Select column for univariate analysis", options=columns)
    analysis_type = st.selectbox("Select analysis type", ["Summary Statistics", "Histogram", "Box Plot", "Violin Plot", "Bar Chart"])

    if analysis_type == "Summary Statistics":
        st.write(data[univariate_col].describe())
    elif analysis_type == "Histogram":
        fig = px.histogram(data, x=univariate_col, color_discrete_sequence=["#636EFA"])
        st.plotly_chart(fig)
    elif analysis_type == "Box Plot":
        fig = px.box(data, y=univariate_col, color_discrete_sequence=["#EF553B"])
        st.plotly_chart(fig)
    elif analysis_type == "Violin Plot":
        fig = px.violin(data, y=univariate_col, color_discrete_sequence=["#00CC96"])
        st.plotly_chart(fig)
    elif analysis_type == "Bar Chart":
        fig = px.bar(data, x=data[univariate_col].value_counts().index, y=data[univariate_col].value_counts().values, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig)

    # Bivariate Analysis
    st.subheader("Bivariate Analysis")
    x_col = st.selectbox("Select X-axis for bivariate analysis", options=columns, index=0)
    y_col = st.selectbox("Select Y-axis for bivariate analysis", options=columns, index=1)
    bivariate_type = st.selectbox("Select bivariate plot type", ["Scatter Plot", "Line Plot", "Correlation Heatmap", "Group Box Plot", "Bar Chart", "3D Scatter Plot"])

    if bivariate_type == "Scatter Plot":
        fig = px.scatter(data, x=x_col, y=y_col, color=y_col, color_continuous_scale="Viridis")
        st.plotly_chart(fig)
    elif bivariate_type == "Line Plot":
        fig = px.line(data, x=x_col, y=y_col, color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig)
    elif bivariate_type == "Correlation Heatmap":
        numeric_data = data.select_dtypes(include=np.number)
        if numeric_data.shape[1] > 1:
            fig = go.Figure(data=go.Heatmap(z=numeric_data.corr().values, x=numeric_data.columns, y=numeric_data.columns, colorscale="Viridis"))
            st.plotly_chart(fig)
        else:
            st.warning("Not enough numeric columns to display a correlation heatmap.")
    elif bivariate_type == "Group Box Plot":
        fig = px.box(data, x=x_col, y=y_col, color=x_col, color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig)
    elif bivariate_type == "Bar Chart":
        fig = px.bar(data, x=x_col, y=y_col, color=x_col, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig)
    elif bivariate_type == "3D Scatter Plot":
        if len(columns) >= 3:
            z_col = st.selectbox("Select Z-axis for 3D scatter plot", options=columns)
            fig = px.scatter_3d(data, x=x_col, y=y_col, z=z_col, color=z_col, color_continuous_scale="Plasma")
            st.plotly_chart(fig)
        else:
            st.warning("Please ensure you have at least three columns for 3D scatter plot.")









