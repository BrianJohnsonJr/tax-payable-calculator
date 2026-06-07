import os
import boto3
from urllib.parse import unquote_plus
from openai import OpenAI
from agent.invoice_agent import InvoiceAgent
from adapters.pdf_renderer import render_pdf_to_images

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    # Read the event
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = unquote_plus(record["s3"]["object"]["key"])
    
    # Download and render
    pdf_bytes = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
    images = render_pdf_to_images(pdf_bytes)
    
    # Load categories
    categories_table = dynamodb.Table(os.environ["TAX_CATEGORIES_TABLE"])
    categories = categories_table.scan()["Items"]
    
    # Run the agent
    agent = InvoiceAgent(OpenAI())
    result = agent.process(images, categories)
    
    # Write result to DynamoDB
    invoices_table = dynamodb.Table(os.environ["INVOICES_TABLE"])
    item = {"invoiceId": key, "status": "DONE"}
    item.update(result.model_dump())
    invoices_table.put_item(Item=item)
    
    return {"statusCode": 200}
    