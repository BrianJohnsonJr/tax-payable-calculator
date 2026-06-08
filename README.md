# Tax Payable Calculator

An agentic service that reads vendor invoices, matches each line item to a tax category, and calculates the tax payable. It was built for the RetailCo scenario, where invoices show up in all kinds of formats including clean PDFs, scanned documents, and handwritten pages.

## Live demo

The app is deployed and running. You can test it in the browser here:

**https://d3vtsj33g291rz.cloudfront.net**

To try it:

1. Open the link above.
2. Click **Choose File** and pick an invoice (PDF or image).
3. Click **Upload**. The status moves through `uploading`, then `processing`, then `done`.
4. After about ten seconds the results appear: the vendor, each line item with its category and tax, and the total tax payable.

The processor is generic, so it works on invoices it has never seen before. The frontend is a React app hosted on S3 and served over HTTPS through CloudFront. Uploads go straight to S3 through a presigned URL, which triggers the processing pipeline described below.

## How it works

A user uploads an invoice file to an S3 bucket. That upload triggers a Lambda function that does the following:

1. Downloads the file and renders each PDF page into an image with PyMuPDF.
2. Loads the tax categories and their rates from DynamoDB.
3. Hands the images to an OpenAI model (gpt-4o) along with the list of categories and a set of tools.
4. The model works through a tool calling loop. It reads every line item, matches it to one category, and calls a `calculate_line_tax` tool to do the math. It never does the arithmetic itself, so the numbers stay exact.
5. The model returns a structured result, which the Lambda writes to a DynamoDB table.

The agent also reads the comments on an invoice. If a note says something like "items are used, no tax required" or "tax already applied", it sets every line tax to zero, marks the invoice as not taxed, and records the reason.

## Why an agent instead of a script

The model is good at the judgment parts, like reading messy or handwritten invoices and deciding which category a product belongs to. It is not reliable at exact math or at remembering precise tax rates. So those jobs are pulled out into small, tested tools that the model calls. The rates live in DynamoDB and the tax math lives in a calculator class, both covered by unit tests. This keeps the results accurate and easy to audit while still letting the model drive.

## Tech stack

The backend is Python 3.12 running on Lambda. It uses the OpenAI SDK for the model, PyMuPDF for rendering PDFs to images, and pydantic for the structured output schema. Data lives in DynamoDB and uploaded files live in S3. The HTTP layer is API Gateway. Everything is described in one AWS SAM template (which is CloudFormation underneath) and deployed by GitHub Actions. The frontend is React.

## Project structure

```
backend/
  src/
    domain/       tax calculator (Decimal math, half up rounding)
    agent/        invoice agent, the calculate_line_tax tool, pydantic schema
    adapters/     dynamodb rate repository, pdf renderer
    handlers/     health endpoint, the s3 processor
    seed/         tax category csv parser and seeder
  tests/          pytest unit tests
infra/
  template.yaml   the SAM / CloudFormation template
data/
  tax_rate_by_category.csv
frontend/         react app
.github/workflows/ deploy pipeline
```

## Running the tests

```
cd backend
pytest
```

The deterministic core is written test first. That covers the tax calculator, the category rate lookup, the csv parser, the schema, and the calculate_line_tax tool.

## Running the agent locally

Put your OpenAI key in a `.env` file at the repo root as `OPENAI_API_KEY`, then run:

```
python backend/src/run_agent.py
```

This renders one invoice PDF, loads the categories from DynamoDB, runs the agent, and prints the result. It is handy for trying the agent without going through S3.

## Seeding the tax categories

The category rates start as a csv and get loaded into DynamoDB once with a small script:

```
python backend/src/seed/tax_categories.py data/tax_rate_by_category.csv <TaxCategoriesTableName>
```

## Deployment

Pushing to the `main` branch triggers the GitHub Actions workflow, which builds the SAM application and deploys the stack to AWS. The build runs on a Linux runner so the native dependencies compile for the Lambda runtime.

The pipeline needs three GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `OPENAI_API_KEY`. The OpenAI key is passed into the template as a parameter at deploy time and never stored in the repo.

## A few design notes

All money is handled with Python's Decimal type and rounded half up to the cent, never with floats. The agent is given the OpenAI client from the outside rather than creating its own, which makes it easy to test with a fake. The same idea is used for the rate repository, which takes the DynamoDB table as a constructor argument.
