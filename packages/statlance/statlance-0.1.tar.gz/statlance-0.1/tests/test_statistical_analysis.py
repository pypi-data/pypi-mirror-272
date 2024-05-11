# statlance/tests/test_statistical_analysis.py

import pytest
from statlance.core.statistical_analysis import summary_statistics, correlation_matrix
from statlance.utils.helper_functions import generate_sample_data

def test_summary_statistics():
    # Generate sample data
    df = generate_sample_data()

    # Test summary_statistics function
    summary_stats = summary_statistics(df)
    
    # Assert that the output is a DataFrame
    assert isinstance(summary_stats, pd.DataFrame)

    # Add more specific test cases as needed

def test_correlation_matrix():
    # Generate sample data
    df = generate_sample_data()

    # Test correlation_matrix function
    correlation_matrix = correlation_matrix(df)
    
    # Assert that the output is a DataFrame
    assert isinstance(correlation_matrix, pd.DataFrame)

    # Add more specific test cases as needed

