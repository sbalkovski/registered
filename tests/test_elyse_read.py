import pytest
import elyse_read
import pandas as pd 
from pathlib import Path

TEST_PDF = Path(__file__) / "support" / 'elyse2_test.pdf'

T = elyse_read.elyse2_pdf_to_text(TEST_PDF, export = False)

def test_columns_parsed():
    # Testing that logic is filtering out the header (Route/Entry/Front) column from the start of each page
    assert ~(T['Signcode'] == 'Route').any()
    assert ~T['Headsign'].str.contains('Entry').any()
    assert ~T['Headsign'].str.contains('Front').any()

def test_headers_removed():
    # Testing that logic is filtering out any rows with 2 blanks / 3
    # Rows with these words are blank otherwise Front: , Led 16x160/10 
    for word in ['Front:', 'Led 16x160/10']:
        assert ~T['Signcode'].str.contains(word).any()
        assert ~T['Headsign'].str.contains(word).any()

def test_no_blank_headsigns():
    # Test that there are no blank headsigns
    assert ~T['Headsign'].isna().any()

def test_type_correct():
    # Test that output is a pandas Dataframe
    assert type(T) == pd.DataFrame