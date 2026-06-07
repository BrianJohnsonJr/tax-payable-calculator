import pytest
from decimal import Decimal
from agent.tools import calculate_line_tax

@pytest.mark.parametrize("amount, rate_percent, expected", [
    (549.45, 10, Decimal("54.95")),
    (100.00, 7, Decimal("7.00")),
    (823.50, 0, Decimal("0.00")),
])
def test_calculate_line_tax(amount, rate_percent, expected):
    assert calculate_line_tax(amount, rate_percent) == expected
    
    
    