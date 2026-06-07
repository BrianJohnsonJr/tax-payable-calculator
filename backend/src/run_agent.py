import boto3
from dotenv import load_dotenv
from openai import OpenAI
from agent.invoice_agent import InvoiceAgent
from adapters.pdf_renderer import render_pdf_to_images

load_dotenv()
client = OpenAI()

TABLE_NAME = "tax-payable-calculator-TaxCategoriesTable-HV8SZAJN7UI8"
table = boto3.resource("dynamodb").Table(TABLE_NAME)
categories = table.scan()["Items"]

agent = InvoiceAgent(client)

PDF_PATH = "data/invoices/25-15886.pdf"
with open(PDF_PATH, "rb") as f:
    pdf_bytes = f.read()
images = render_pdf_to_images(pdf_bytes)
result = agent.process(images, categories)
print(result)

