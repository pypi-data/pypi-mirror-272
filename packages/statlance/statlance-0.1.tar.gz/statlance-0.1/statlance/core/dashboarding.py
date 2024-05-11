# statlance/core/dashboarding.py
import streamlit as st
import pandas as pd
from statlance.core.data_processing import upload_or_connect, preprocess_data
from statlance.core.statistical_analysis import summary_statistics, correlation_matrix
from statlance.core.visualizations import histogram, box_plot, scatter_plot, correlation_heatmap
from statlance.core.wrangling import handle_missing_values, handle_duplicates, handle_outliers

def main():
    st.set_page_config(layout="wide")
    st.title("Statlance Dashboard")

    # Sidebar navigation
    page = st.sidebar.radio("Navigation", ["Data Processing", "Statistical Analysis", "Visualizations"])

    if page == "Data Processing":
        st.header("Data Processing")

        # Upload or connect to data
        df = upload_or_connect()

        if df is not None:
            st.subheader("Raw Data")
            st.write(df)

            # Data preprocessing options
            st.subheader("Data Preprocessing")
            processed_data = preprocess_data(df)
            st.write(processed_data)

    elif page == "Statistical Analysis":
        st.header("Statistical Analysis")

        # Upload or connect to data
        df = upload_or_connect()

        if df is not None:
            # Statistical analysis options
            st.subheader("Summary Statistics")
            st.write(summary_statistics(df))

            st.subheader("Correlation Matrix")
            st.write(correlation_matrix(df))

            # Add more statistical analysis options as needed...

    elif page == "Visualizations":
        st.header("Visualizations")

        # Upload or connect to data
        df = upload_or_connect()

        if df is not None:
            # Data preprocessing
            df = preprocess_data(df)

            # Visualization options
            st.subheader("Histogram")
            column = st.selectbox("Select Column for Histogram", df.columns)
            histogram(df, column)

            st.subheader("Box Plot")
            x = st.selectbox("Select X-axis Column", df.columns)
            y = st.selectbox("Select Y-axis Column", df.columns)
            box_plot(df, x, y)

            # Add more visualization options as needed...

if __name__ == "__main__":
    main()

