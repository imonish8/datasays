import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("CSV Data Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.write(df.head())

    # Select columns
    x_column = st.selectbox("Select X-axis column", df.columns)
    y_column = st.selectbox("Select Y-axis column", df.columns)

    # Select plot type
    plot_type = st.selectbox(
        "Select Plot Type",
        ("Line Plot", "Bar Plot", "Scatter Plot")
    )

    # Generate plot
    if st.button("Generate Plot"):
        if plot_type == "Line Plot":
            fig = px.line(df, x=x_column, y=y_column)
        elif plot_type == "Bar Plot":
            fig = px.bar(df, x=x_column, y=y_column)
        elif plot_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column)
        else:
            st.error("Invalid plot type selected.")

        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Please upload a CSV file to get started.")