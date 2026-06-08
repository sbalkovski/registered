import pytest
from pathlib import Path
from registered.stop_comparison import *

NEXT_RATING_PATH = Path(__file__).parent / "support" / "rating_next" / "Combine"
PREV_RATING_PATH = Path(__file__).parent / "support" / "rating_prev" / "Combine"

def test_stop_comparison_output(capsys):
    # Create a fake argparse Namespace
    args = argparse.Namespace(
        CURRENT=PREV_RATING_PATH,
        NEXT=NEXT_RATING_PATH
    )

    main(args)

    actual_output = capsys.readouterr().out
    expected_output_file_path = Path(__file__).parent / "support" / "stop_comparison" / "valid_stop_comparison.txt"

    assert actual_output.strip() == expected_output_file_path.read_text(encoding="utf-16").strip()