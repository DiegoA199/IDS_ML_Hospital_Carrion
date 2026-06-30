import pandas as pd

from src.ui.pages import DEMO_DATASET_PATH


def test_demo_dataset_is_available_for_the_product_tour():
    assert DEMO_DATASET_PATH.is_file()


def test_demo_dataset_has_features_and_multiclass_target():
    dataframe = pd.read_csv(DEMO_DATASET_PATH)

    assert {"duration", "src_bytes", "dst_bytes", "protocol", "service", "label"}.issubset(dataframe.columns)
    assert dataframe["label"].nunique() >= 2
