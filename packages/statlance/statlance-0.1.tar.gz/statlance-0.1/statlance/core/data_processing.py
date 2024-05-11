# statlance/core/data_processing.py
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from statlance.core import wrangling

def upload_or_connect():
    """
    Function to prompt the user to upload a file or connect to a database using Streamlit.
    """
    st.title("Statlance - Data Processing")

    # Display options for file upload or database connection
    option = st.radio("Choose an option:", ("Upload a file", "Connect to a database"))

    if option == "Upload a file":
        # Display file upload widget
        uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xls', 'xlsx', 'json', 'txt', 'sql'])

        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1]

            if file_extension in ['csv', 'txt']:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(uploaded_file, encoding="utf-8")
            elif file_extension == 'json':
                df = pd.read_json(uploaded_file, encoding="utf-8")
            elif file_extension == 'sql':
                # Read SQL file
                df = read_sql_file(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload a CSV, Excel, JSON, TXT, or SQL file.")
                return

            st.success("File uploaded successfully.")
            return df

        else:
            st.warning("Please upload a file.")

    elif option == "Connect to a database":
        database_url = st.text_input("Enter the database URL:")
        query = st.text_area("Enter the SQL query to fetch data:")

        if st.button("Connect"):
            # Call the load_data_from_sql function with the provided database URL and query
            df = load_data_from_sql(database_url, query)
            return df

    else:
        st.error("Invalid option selected.")



def load_data(file_path):
    """
    Function to load data from a file into a pandas DataFrame.
    It handles various file formats and languages.
    """
    # Check if file_path is provided
    if file_path is None:
        raise ValueError("File path is required.")
    
    # Determine the file type and use the appropriate pandas function to read it
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, encoding="utf-8")
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path, encoding="utf-8")
    elif file_path.endswith(('.json')):
        df = pd.read_json(file_path, encoding="utf-8")
    elif file_path.endswith(('.txt')):
        df = pd.read_csv(file_path, delimiter='\t', encoding="utf-8")
    else:
        raise ValueError("Unsupported file type")
    
    return df


def load_data_from_sql(database_url, query):
    """
    Function to load data from a SQL database into a pandas DataFrame.
    """
    # Use SQLAlchemy to create an engine and read data using pandas
    engine = create_engine(database_url)
    df = pd.read_sql(query, engine)
    return df

  
# statlance/core/data_wrangling.py
import streamlit as st
import pandas as pd
from statlance.core import wrangling

def data_wrangling(df):
    """
    Function to perform data wrangling transformations based on user choice.
    """
    st.title("Statlance - Data Wrangling")

    # Display options for data wrangling transformations
    options = st.multiselect("Select data wrangling transformations:", [
        "Handle Missing Values",
        "Handle Duplicates",
        "Handle Outliers",
        "Data Type Conversion",
        "Feature Engineering",
        "Normalization/Scaling",
        "Encoding Categorical Variables",
        "Grouping and Aggregation",
        "Pivot Tables",
        "Reshaping Data",
        "Merge and Join",
        "Handling Time Series Data",
        "Text Data Processing"
    ])

    # Apply selected transformations
    for option in options:
        if option == "Handle Missing Values":
            df = wrangling.handle_missing_values(df)
        elif option == "Handle Duplicates":
            df = wrangling.handle_duplicates(df)
        elif option == "Handle Outliers":
            df = wrangling.handle_outliers(df)
        elif option == "Data Type Conversion":
            df = wrangling.data_type_conversion(df)
        elif option == "Feature Engineering":
            df = wrangling.feature_engineering(df)
        elif option == "Normalization/Scaling":
            df = wrangling.normalization_scaling(df)
        elif option == "Encoding Categorical Variables":
            df = wrangling.encode_categorical_variables(df)
        elif option == "Grouping and Aggregation":
            df = wrangling.grouping_and_aggregation(df)
        elif option == "Pivot Tables":
            df = wrangling.pivot_tables(df)
        elif option == "Reshaping Data":
            df = wrangling.reshape_data(df)
        elif option == "Merge and Join":
            df = wrangling.merge_and_join(df)
        elif option == "Handling Time Series Data":
            df = wrangling.handle_time_series_data(df)
        elif option == "Text Data Processing":
            df = wrangling.text_data_processing(df)

    st.success("Data wrangling transformations applied successfully.")
    return df
