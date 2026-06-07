from decimal import Decimal
from agent.schema import InvoiceResult, LineItem

def test_invoice_result_constructs_with_defaults():
    line_item_schema = LineItem(description="Shirt", amount=Decimal("100.00"), category="Clothing", tax_rate=Decimal("7"), tax_amount=Decimal("7.00"))
    invoice_results_schema = InvoiceResult(vendor="Alpha Imports", total_tax=Decimal("7.00"), tax_applied=True, line_items=[line_item_schema])

    assert invoice_results_schema.override_reason is None
    assert invoice_results_schema.line_items[0].category == "Clothing"