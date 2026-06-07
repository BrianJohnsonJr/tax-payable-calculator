from decimal import Decimal
from seed.tax_categories import parse_tax_categories

def test_parse_tax_categories():
    csv_string = """Index,Category,Tax Rate (%)
1,Fresh Produce,0
6,Soft Drinks,6.5"""
    
    parsed_csv_file = parse_tax_categories(csv_string)
    assert parsed_csv_file == [
    {"category": "Fresh Produce",
     "rate": Decimal("0")},
    {"category": "Soft Drinks",
     "rate": Decimal("6.5")}    
    ]