from src.utils.formatters import as_percent, compact_int


def test_as_percent_handles_none_fraction_and_percent_values():
    assert as_percent(None) == "0.00%"
    assert as_percent(0.9345, digits=1) == "93.5%"
    assert as_percent(93.45, digits=1) == "93.5%"


def test_compact_int_handles_none_and_numeric_values():
    assert compact_int(None) == "0"
    assert compact_int(1200) == "1,200"
    assert compact_int(1200.9) == "1,200"
