import pandas as pd
import pytest
from src.pipeline import get_rows_to_update

def test_get_rows_to_update_filters_correctly():
    # Create test data
    df = pd.DataFrame({
        'Well Name': ['Well A', 'Well B', 'Well C'],
        'Well Type': ['Type1', 'Type2', 'Type3'],
        'DMS': ['SW DEV', 'No', None],
        'Plan DDPTF': [1.0, 2.0, 3.0],
        'Plan DCPF': [None, None, None],
        'Plan WCPF': [None, None, None],
        'Actual DDPTF': [None, None, None],
        'Actual DCPF': [None, None, None],
        'Actual WCPF': [None, None, None],
    })
    
    result = get_rows_to_update(df)
    
    # Assert only Well A passes (valid DMS + has data)
    assert len(result) == 2
    assert result.iloc[0]['Well Name'] == 'Well A'

def test_get_rows_to_update_empty():
    df = pd.DataFrame({
        'Well Name': [],
        'Well Type': [],
        'DMS': [],
        'Plan DDPTF': [],
        'Plan DCPF': [],
        'Plan WCPF': [],
        'Actual DDPTF': [],
        'Actual DCPF': [],
        'Actual WCPF': [],
    })

    result = get_rows_to_update(df)
    assert len(result) == 0
