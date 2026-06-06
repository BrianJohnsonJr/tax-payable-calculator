import csv
import io
import boto3
from decimal import Decimal
import sys

def parse_tax_categories(csv_text):
    string_to_file = io.StringIO(csv_text)
    reader = csv.DictReader(string_to_file)
    results = []
    for row in reader:
        row_dictionary = {
            "category": row["Category"], "rate": Decimal(row["Tax Rate (%)"])
        }
        results.append(row_dictionary)
        
    return results

def write_tax_categories(items, table_name):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table(table_name)
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)
            
def main():
    csv_path = sys.argv[1]
    table_name = sys.argv[2]
    
    with open(csv_path) as f:
        text = f.read()
        
    items = parse_tax_categories(text)
    write_tax_categories(items, table_name)
    print(f"Wrote {len(items)} categories")
    
if __name__ == '__main__':
    main()        