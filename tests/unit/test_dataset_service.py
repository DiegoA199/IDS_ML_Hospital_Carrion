import pandas as pd
import pytest

from src.core.exceptions import DatasetValidationError
from src.domain.services.dataset_service import build_dataset_profile, calculate_quality_score, validate_dataset
from src.utils.validators import find_missing_columns


def test_validate_dataset_rejects_empty_dataframe():
    with pytest.raises(DatasetValidationError):
        validate_dataset(pd.DataFrame())


def test_find_missing_columns_reports_absent_names():
    df = pd.DataFrame({"a": [1]})
    assert find_missing_columns(df, ["a", "b"]) == ["b"]


def test_profile_counts_nulls_and_duplicates():
    df = pd.DataFrame({"a": [1, 1, None], "b": ["x", "x", "y"]})
    profile = build_dataset_profile(df)
    assert profile.missing_total == 1
    assert profile.duplicated_rows == 1
    assert 0 <= calculate_quality_score(profile) <= 100

