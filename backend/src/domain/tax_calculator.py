from decimal import Decimal
from decimal import ROUND_HALF_UP

class TaxCalculator:
    def line_tax(self, amount, rate_percent):
        raw_tax_amount = rate_percent/100 * amount
        round_cents = raw_tax_amount.quantize(Decimal('0.01'), rounding = ROUND_HALF_UP)
        return round_cents