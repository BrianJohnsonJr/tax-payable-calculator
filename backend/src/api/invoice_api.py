import json
from decimal import Decimal
from uuid import uuid4

def json_default(value):
    if isinstance(value, Decimal): 
        return str(value)
    else:
        raise TypeError
    
def response(status, data):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "*"
        },
        "body": json.dumps(data, default=json_default)
    }
    
class InvoiceApi:
    def __init__(self, s3, bucket, invoices_table, id_generator):
        self.s3 = s3
        self.bucket = bucket
        self.invoices_table = invoices_table
        self.id_generator = id_generator
        
    def create_upload_url(self, filename):
        key = f"uploads/{self.id_generator()}-{filename}"
        url = self.s3.generate_presigned_url("put_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=3600)
        return {"url": url, "key": key}
    
    def list_invoices(self):
        items = self.invoices_table.scan()["Items"]
        return items
    def get_invoice(self, invoice_id):
        result = self.invoices_table.get_item(Key={"invoiceId": invoice_id})
        return result.get("Item")
    
    def handle(self, event):
        method = event["httpMethod"]
        path = event["resource"]
        
        if method == "POST" and path == "/uploads":
            body = json.loads(event["body"])
            filename = body["filename"]
            data = self.create_upload_url(filename)
            return response(200, data)
        elif method == "GET" and path == "/invoices":
            data = self.list_invoices()
            return response(200, data)
        elif method == "GET" and path == "/invoices/{invoiceId}":
            invoice_id = event["pathParameters"]["invoiceId"]
            item = self.get_invoice(invoice_id)
            if item is None:
                return response(404, {"error": "not found"})
            else:
                return response(200, item)
        else:
            return response(404, {"error": "route not found"})