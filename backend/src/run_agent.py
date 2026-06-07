import boto3
from dotenv import load_dotenv
from openai import OpenAI
from agent.invoice_agent import InvoiceAgent

load_dotenv()
client = OpenAI()

TABLE_NAME = "tax-payable-calculator-TaxCategoriesTable-HV8SZAJN7UI8"
table = boto3.resource("dynamodb").Table(TABLE_NAME)
categories = table.scan()["Items"] 

invoice_text = """Alpha Imports — INVOICE 25-12788

DESCRIPTION, QUANTITY, ITEM PRICE, AMOUNT
Coca-Cola Original – 12 Pack (12 fl oz Cans), 3, $8.99, $26.97
Pepsi Cola – 12 Pack (12 fl oz Cans), 4, $8.79, $35.16
Sprite Lemon-Lime Soda – 12 Pack, 5, $8.99, $44.95
Dr Pepper – 12 Pack, 3, $8.79, $26.37
Mountain Dew – 12 Pack, 10, $8.79, $87.90
Diet Coke – 12 Pack, 11, $8.99, $98.89
Starbucks Pike Place Roast Ground Coffee – 12 oz Bag, 5, $11.99, $59.95
TOTAL $380.19

OTHER COMMENTS
1. Total payment due in 30 days
2. Please include the invoice number on your check
Make all checks payable to Alpha Imports"""


agent = InvoiceAgent(client)
result = agent.process(invoice_text, categories)
print(result)

