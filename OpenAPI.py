from openai import OpenAI
OPENAI_API_KEY = "Your OpenAI Key"
client = OpenAI(api_key=OPENAI_API_KEY)

import pandas as pd

# Read the Excel file
file_path = 'D:\\Rent-Roll-T12\\Bellaire Oaks - April 2024 T-12 - Copy.xlsx'
data = pd.read_excel(file_path)
prompt = pd.DataFrame(data)#.to_string()

system_prompt = """
You are a helpful assistant working as a data extractor. Your task is to analyze the provided data and find specific values. You must strictly analyze the provided data without skipping any characters.

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

pppp="""
1. you are a helpful assistant working as a data extractor, your task is to analyze the provided data and find these values:
2. You have to strictly analyze the provided data without skipping the any charactor:
-------------------Projected--Income--------------------------------------
- Projected Other Income: Example: $ 1,000
-Gas & Electric Income: Example: $ 1,000
-Late Charges: Example: $ 1,000
-Maid/Housekeeping Services Income: Example: $ 1,000
-Lease Termination Fees Income: Example: $ 1,000
-Application Fees Income: Example: $ 1,000
-Pet Rent Fees Income: Example: $ 1,000
-Parking Fees Income: Example: $ 1,000
-Other Charges: Example: $ 1,000
-------------------------------------------Projected--Utilities--------------------------------------------------
-Projected Utilities: Example: $ 1,000
-Gas & Electric: Example: $ 1,000
-Water & Sewer: Example: $ 1,000
-Trash : Example: $ 1,000
-Other Charges: Example: $ 1,000
-------------------------------------------Projected Operating Expenses-------------------------------------------------------------------------
-Projected Operating Expenses: Example: $ 1,000
-Management Fee : Example: $ 1,000
-Total Payroll Fees: Example: $ 1,000
-General & Administrative: Example: $ 1,000
-Legal & Accounting: Example: $ 1,000
-Marketing: Example: $ 1,000
-Repairs & Maintenance: Example: $ 1,000
-Turnover: Example: $ 1,000
-Contract Services: Example: $ 1,000
-Total Utilities: Example: $ 1,000
-Utility Reimbursements: Example: $ 1,000
-Property Taxes: Example: $ 1,000
-Insurance: Example: $ 1,000
-Capital Reserve: Example: $ 1,000

Note: Give the json format as output, don't use the as values of given example.
"""

# Combine the system prompt with the DataFrame prompt


messages=[
{"role": "system", "content": system_prompt},
{"role": "user", "content": str(prompt)}
]


completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        )
print(completion.choices[0].message.content)


