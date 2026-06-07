from pydantic import BaseModel
from decimal import Decimal

class LineItem(BaseModel):
    
    description: str
    amount: Decimal
    category: str
    tax_rate: Decimal
    tax_amount: Decimal
    
    
class InvoiceResult(BaseModel):
    vendor: str
    total_tax: Decimal
    tax_applied: bool
    override_reason: str | None = None
    line_items: list[LineItem]