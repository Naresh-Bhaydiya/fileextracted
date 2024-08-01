import pandas as pd
import replicate

# Read the Excel file
file_path = 'D:\\Rent-Roll-T12\\Bellaire Oaks - April 2024 T-12 - Copy.xlsx'
data = pd.read_excel(file_path)
prompt = pd.DataFrame(data)#.to_string()

REPLICATE_API_TOKEN = "REPLICATE_API_KEY"


# Your API token from Replicate
api_token = REPLICATE_API_TOKEN

system_prompt =  """You are a helpful assistant working as a data extractor. Your task is to analyze the provided data and find specific values. You must strictly analyze the provided data without skipping any characters.

Extract the following information and present it in JSON format:

1. Projected Income:
   - Projected Other Income
   - Gas & Electric Income
   - Late Charges
   - Maid/Housekeeping Services Income
   - Lease Termination Fees Income
   - Application Fees Income
   - Pet Rent Fees Income
   - Parking Fees Income
   - Other Charges

2. Projected Utilities:
   - Projected Utilities (total)
   - Gas & Electric
   - Water & Sewer
   - Trash
   - Other Charges

3. Projected Operating Expenses:
   - Projected Operating Expenses (total)
   - Management Fee
   - Total Payroll Fees
   - General & Administrative
   - Legal & Accounting
   - Marketing
   - Repairs & Maintenance
   - Turnover
   - Contract Services
   - Total Utilities
   - Utility Reimbursements
   - Property Taxes
   - Insurance
   - Capital Reserve

Important: 
- Provide the output in JSON format.
- Do not use the example values given (such as "$ 1,000").
- Use the actual values found in the provided data.
- If a value is not present in the data, use omit the field.

Analyze the given data carefully and extract the requested information accurately.   
"""

# Combine the system prompt with the DataFrame prompt
full_prompt = f"system\n\n{system_prompt}user\n\n{prompt}assistant\n\n"

input_data = {
    "system_prompt": system_prompt,
    "prompt": str(prompt),
    "max_new_tokens": 512,
    "prompt_template": "system\n\n{system_prompt}user\n\n{prompt}assistant\n\n"
}

client = replicate.Client(api_token=api_token)

# Use the predict method to get the prediction result
model = client.models.get("meta/meta-llama-3-8b-instruct")
model_version = "meta/meta-llama-3-8b-instruct"  # Adjust this to the correct model version if needed

prediction = client.run(f"{model_version}", input=input_data)


for event in prediction:
    print(event, end="")
