import json
from agent.tools import calculate_line_tax
from agent.schema import InvoiceResult

class InvoiceAgent:
    def __init__(self, client):
        self.client = client
        
    def process(self, invoice_text, categories):
        messages = [
            {"role": "system", "content": build_system_prompt(categories)},
            {"role": "user", "content": invoice_text},
        ]
        
        for i in range(10):
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                tools=CALCULATE_TOOL,
                response_format=InvoiceResult,
            )
            message = completion.choices[0].message
            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    result = calculate_line_tax(args["amount"], args["rate_percent"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result),
                    })
            else:
                return message.parsed

CALCULATE_TOOL = [
    {
        "type": "function",
        "function": {
            "name": "calculate_line_tax",
            "description": "Calculate the tax for one line item from its amount and tax rate percent.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "amount":       {"type": "number", "description": "the line's extended amount in dollars"},
                    "rate_percent": {"type": "number", "description": "the tax rate as a percent, e.g. 7 for 7%"}
                },
                "required": ["amount", "rate_percent"],
                "additionalProperties": False
            }
        }
    }
]


def build_system_prompt(categories):
    category_lines = "\n".join(f"- {c['category']}: {c['rate']}%" for c in categories)
    prompt = f"""You are a tax-categorization agent for invoices.

For each line item: match it to EXACTLY ONE of the tax categories below, then call the
calculate_line_tax tool with the line's amount and that category's rate. NEVER compute tax
yourself — always use the tool.

If the invoice has any comment indicating tax should not apply (e.g. "do not tax", "tax already
applied", "used goods"), set every line's tax to 0, set tax_applied to false, and record the
reason in override_reason.

When finished, return the complete InvoiceResult.

Available tax categories:
{category_lines}
"""
    return prompt

