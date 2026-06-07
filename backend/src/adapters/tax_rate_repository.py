
class TaxRateRepository:
    def __init__(self, table):
        self.table = table
        
    def get_rate(self, category):
        get_category = self.table.get_item(Key={"category":category})
        item = get_category.get("Item")
        if item is None:
            raise ValueError(f"{category} is unknown")
        else:
            return item["rate"]