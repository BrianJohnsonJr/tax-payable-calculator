from decimal import Decimal
from adapters.tax_rate_repository import TaxRateRepository
import pytest

class FakeTable:
    def __init__(self, response):
        self.response = response
        
    def get_item(self, Key):
        return self.response

def test_get_rate_returns_rate_for_known_category():
    repo = TaxRateRepository(FakeTable({"Item": {"category": "Alcoholic Beverages", "rate": Decimal("10")}}))
    rate = repo.get_rate("Alcoholic Beverages")
    assert rate == Decimal("10")
    
def test_get_rate_raises_for_unknown_category():
    repo = TaxRateRepository(FakeTable({}))
    with pytest.raises(ValueError):
        repo.get_rate("Nonexistent Category")