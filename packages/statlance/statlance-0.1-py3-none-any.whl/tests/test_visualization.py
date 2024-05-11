# statlance/tests/test_visualization.py

import pytest
from statlance.core.visualization import histogram
from statlance.utils.helper_functions import generate_sample_data

def test_histogram():
    # Generate sample data
    df = generate_sample_data()

    # Test histogram function
    hist = histogram(df, 'A')
    
    # Assert that the output is a plot object
    assert isinstance(hist, plt.Axes)

    # Add more specific test cases as needed

