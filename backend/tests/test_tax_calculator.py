import pytest
from decimal import Decimal    
from domain.tax_calculator import TaxCalculator

@pytest.mark.parametrize("amount, rate_percent, expected", [
    (Decimal('823.50'), Decimal('0'), Decimal('0.00')),
    (Decimal('100.00'), Decimal('7'), Decimal('7.00')),
    (Decimal('549.45'), Decimal('10'), Decimal('54.95')),
    (Decimal('100.00'), Decimal('6.5'), Decimal('6.50')),
])
def test_line_tax_returns_expected_tax(amount, rate_percent, expected):
    calculate_tax = TaxCalculator().line_tax(amount, rate_percent)
    assert calculate_tax == expected