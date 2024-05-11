# statlance/tests/test_data_processing.py

import pytest
from statlance.core.data_processing import preprocess_data
from statlance.utils.helper_functions import generate_sample_data

def test_preprocess_data():
    # Generate sample data
    df = generate_sample_data()

    # Test preprocess_data function
    processed_data = preprocess_data(df)
    
    # Assert that the output is a DataFrame
    assert isinstance(processed_data, pd.DataFrame)

    # Add more specific test cases as needed

