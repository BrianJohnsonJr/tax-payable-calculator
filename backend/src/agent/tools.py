from decimal import Decimal
from domain.tax_calculator import TaxCalculator

def calculate_line_tax(amount, rate_percent):
    amount_decimal = Decimal(str(amount))
    rate_decimal = Decimal(str(rate_percent))
    return TaxCalculator().line_tax(amount_decimal, rate_decimal)

