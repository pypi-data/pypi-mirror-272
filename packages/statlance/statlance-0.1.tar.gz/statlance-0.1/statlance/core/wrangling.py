# statlance/core/wrangling.py
import streamlit as st
import pandas as pd

# handle_missing_values:
def handle_missing_values(df, columns=None):
    """
    Function to handle missing values in specified columns or the entire DataFrame.
    """
    if columns is None:
        df = df.dropna()
    else:
        df[columns] = df[columns].dropna()
    return df

# handle_duplicats
def handle_duplicates(df, columns=None):
    """
    Function to handle duplicates in specified columns or the entire DataFrame.
    """
    if columns is None:
        df = df.drop_duplicates()
    else:
        df = df.drop_duplicates(subset=columns)
    return df

# handle_outliers

def handle_outliers(df, columns=None):
    """
    Function to handle outliers in specified columns or the entire DataFrame.
    """
    # Implement outlier detection and removal logic here
    return df

# data_type_conversion
def data_type_conversion(df, columns=None, new_data_type='float64'):
    """
    Function to convert data types of specified columns or the entire DataFrame.
    """
    if columns is None:
        df = df.astype(new_data_type)
    else:
        df[columns] = df[columns].astype(new_data_type)
    return df

# feature_engineering
def feature_engineering(df, columns=None):
    """
    Function to perform feature engineering on specified columns or the entire DataFrame.
    """
    # Implement feature engineering logic here
    return df

# normalization_scaling
def normalization_scaling(df, columns=None):
    """
    Function to normalize or scale specified columns or the entire DataFrame.
    """
    # Implement normalization or scaling logic here
    return df


# encode_categorical_variables:
def encode_categorical_variables(df, columns=None):
    """
    Function to encode categorical variables in specified columns or the entire DataFrame.
    """
    # Implement encoding logic here
    return df

# grouping_and_aggregation:
def grouping_and_aggregation(df, columns=None, by=None):
    """
    Function to perform grouping and aggregation on specified columns or the entire DataFrame.
    """
    # Implement grouping and aggregation logic here
    return df

# reshape_data
def reshape_data(df, columns=None):
    """
    Function to reshape data in specified columns or the entire DataFrame.
    """
    # Implement data reshaping logic here
    return df

# merge_and_join
def merge_and_join(df, other_df, on=None, how='inner'):
    """
    Function to merge and join the DataFrame with another DataFrame.
    """
    # Implement merge and join logic here
    return df

# text_data_processing
def text_data_processing(df, columns=None):
    """
    Function to process text data in specified columns or the entire DataFrame.
    """
    # Implement text data processing logic here
    return df

# Pivot_tables
def pivot_tables(df, index=None, columns=None, values=None, aggfunc='mean'):
    """
    Function to create pivot tables from the DataFrame.
    """
    # Create pivot table
    df = pd.pivot_table(df, index=index, columns=columns, values=values, aggfunc=aggfunc)
    
    return df