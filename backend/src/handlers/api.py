import os
import boto3
from uuid import uuid4
from api.invoice_api import InvoiceApi

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
invoices_table = dynamodb.Table(os.environ["INVOICES_TABLE"])
bucket = os.environ['INVOICE_BUCKET']
api = InvoiceApi(s3, bucket, invoices_table, lambda: str(uuid4()))

def lambda_handler(event, context):
    return api.handle(event)