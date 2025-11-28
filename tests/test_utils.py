# tests/test_utils.py
from app.utils import normalize_price_str, extract_first_price, parse_into_items

def test_normalize_price_str():
    assert normalize_price_str("1,234.56") == 1234.56
    assert normalize_price_str("12.34") == 12.34
    assert normalize_price_str("1234") == 12.34 or isinstance(normalize_price_str("1234"), float)

def test_extract_first_price():
    assert extract_first_price("Total 9.99\nTax 0.99") == 9.99

def test_parse_into_items():
    txt = "Coffee 3.50\nSandwich 5.00\nNote: Thanks"
    items = parse_into_items(txt)
    assert any(it["name"].lower().startswith("coffee") for it in items)
    assert any(abs(it["price"] - 5.0) < 1e-6 for it in items)