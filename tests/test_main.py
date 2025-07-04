import pytest
from main import filter_rows, aggregate_column, is_number

rows = [
    {"name": "iphone 15 pro", "brand": "apple", "price": "999", "rating": "4.9"},
    {"name": "galaxy s23 ultra", "brand": "samsung", "price": "1199", "rating": "4.8"},
    {"name": "redmi note 12", "brand": "xiaomi", "price": "199", "rating": "4.6"},
    {"name": "poco x5 pro", "brand": "xiaomi", "price": "299", "rating": "4.4"},
]

def test_filter_rows():
    res = filter_rows(rows, "price", ">", "500")
    assert len(res) == 2

def test_aggregate_avg():
    assert aggregate_column(rows, "price", "avg") == pytest.approx(674.0, 0.001)

def test_aggregate_min():
    assert aggregate_column(rows, "price", "min") == 199

def test_aggregate_max():
    assert aggregate_column(rows, "price", "max") == 1199

def test_aggregate_invalid_func():
    with pytest.raises(ValueError):
        aggregate_column(rows, "price", "sum")

def test_filter_invalid_operator():
    with pytest.raises(ValueError):
        filter_rows(rows, "price", "!", "100")

def test_filter_rows_text():
    res = filter_rows(rows, "name", "=", "iphone 15 pro")
    assert len(res) == 1
    assert res[0]["name"] == "iphone 15 pro"
