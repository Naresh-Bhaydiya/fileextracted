import streamlit as st
import pandas as pd
import csv
import cohere
from decouple import config

COHERE_API_KEY = config("COHERE_API_KEY")

def convert_excel_to_csv_file():
    try:
        # Specify the path to your .xlsx file
        xlsx_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
        # Read the .xlsx file
        if xlsx_file is not None:
            df = pd.read_excel(xlsx_file, engine='openpyxl')
            # Specify the path for the output .csv file
            csv_file = 'T12csvfile.csv'
            # Save the dataframe as a .csv file
            df.to_csv(csv_file, index=False)
            return csv_file
    except Exception as e:
        st.error(f"Error converting Excel to CSV: {e}")
    return None

def convert_csv_to_text(csv_file):
    try:
        if csv_file is not None:
            text_file = "T12_Textfile.txt"
        
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                
                with open(text_file, 'w', newline='', encoding='utf-8') as outfile:
                    for row in csv_reader:
                        # Join the elements of each row with a tab separator
                        line = "\t".join(row)
                        # Write the line to the text file
                        outfile.write(line + "\n")
            return text_file
    except Exception as e:
        st.error(f"Error converting CSV to text: {e}")
    return None

def main():
    try:
        csv_file = convert_excel_to_csv_file()
        if csv_file is not None:
            text_file = convert_csv_to_text(csv_file)

            if text_file is not None:
                with open(text_file, 'r', encoding='utf-8') as file:
                    prompt = file.read()                
                    system_prompt = """
You are a data extractor. Your goal is to extract and calculate total values for the fields related to Annual Rental Income and TurnOver Make Ready from the provided data, which contains values for 12 months. Here are the detailed instructions:

1. Fields for Extraction:

A. Annual Rental Income Fields:

1. GROSS_MARKET_RENT: Total rental income based on the market rate.
2. Net_Gross_Potential_Income: Net income considering potential gross income.
3. TOTAL_GROSS_POTENTIAL_RENT: Sum of all potential gross rents.
4. Gross_Rent: Total gross rent without any deductions.
5. Potential_Rent: The estimated potential rent.
6. Total_Gross_Potential_Rents: Cumulative total of gross potential rents.
7. Total_Rental_Income: Total income from rental properties.
8. Potential_Rental_Income: Estimated potential income from rents.
9. Gross_Potential_Rent: Potential gross rent for properties.
10. GROSS_POTENTIAL_PER_LEASE: Gross potential rent per lease agreement.
11. Total_RENTS: Total amount received from rents.
12. Apartment_Rent_Income: Income specifically from apartment rents.
13. Total_Rent_Per_Schedule: Total rent as per the rent schedule.
14. Rental_Income: Overall rental income.
15. Total_Gross_Rent_Income: Total income from gross rents.
16. Gross_potential_rent_revenue: Revenue from gross potential rents.
17. TOTAL_RENTAL_REVENUE: Total revenue from rental properties.
18. Net_Potential_Rent: Net potential rent value.
19. Total_Gross_Possible_Rent: Total gross rent that is possible.
20. Total_Net_Rental_Income: Total net income from rentals.

B. TurnOver Make Ready Fields:

1. MARKET_READY_EXPENSES: Expenses incurred to make properties market-ready.
2. Total_Make_Ready_Redecorating: Total expenses for redecorating to make ready.
3. Total_MakeReady: Total expenses for making properties ready.
4. TURNOVER_COSTS: Costs associated with property turnover.
5. Total_Apartment_Turnover: Total costs related to apartment turnover.
6. Total_Turnkey_Expense: Total expenses for turnkey operations.
7. Turnover_Expenses: Overall expenses related to turnover.
8. MAKE_READY: Expenses related to preparing properties.
9. Make_Ready_Expense: Specific expenses for making properties ready.
10. Apartment_Turnover: Costs related to turnover of apartments.
11. Redecorating_turnover_expense: Expenses specifically for redecorating during turnover.
12. Total_Make_Ready_Redecorating: Total expenses for redecorating to make ready.
13. SUBTOTAL_MAINT_TURNOVER: Subtotal of maintenance turnover costs.
14. TURNOVER: Turnover-related costs (repeated field).
15. TOTAL_APARTMENT_TURNOVER_COSTS: Total costs for apartment turnover.
16. TOTAL_TURNOVER_MAINTENANCE: Total maintenance costs for turnover.
17. TOTAL_RECONDITIONING: Total costs for reconditioning.

2. Instructions:

~If a total value for a field is missing, calculate it by summing up the values for the 12 months.
~If the total value is present in the provided data, use it directly.
~Do not generate any random values; use only the data provided.
~ Ensure no field values is empty or null.
Output Format:
{
    "Annual_Rental_Income": {
        "GROSS_MARKET_RENT": "",
        "Net_Gross_Potential_Income": "",
        "TOTAL_GROSS_POTENTIAL_RENT": "",
        "Gross_Rent": "",
        "Potential_Rent": "",
        "Total_Gross_Potential_Rents": "",
        "Total_Rental_Income": "",
        "Potential_Rental_Income": "",
        "Gross_Potential_Rent": "",
        "GROSS_POTENTIAL_PER_LEASE": "",
        "Total_RENTS": "",
        "Apartment_Rent_Income": "",
        "Total_Rent_Per_Schedule": "",
        "Rental_Income": "",
        "Total_Gross_Rent_Income": "",
        "Gross_potential_rent_revenue": "",
        "TOTAL_RENTAL_REVENUE": "",
        "Net_Potential_Rent": "",
        "Total_Gross_Possible_Rent": "",
        "Total_Net_Rental_Income": ""
    },
    "TurnOver_Make_Ready": {
        "MARKET_READY_EXPENSES": "",
        "Total_Make_Ready_Redecorating": "",
        "Total_MakeReady": "",
        "TURNOVER_COSTS": "",
        "Total_Apartment_Turnover": "",
        "Total_Turnkey_Expense": "",
        "Turnover_Expenses": "",
        "MAKE_READY": "",
        "Make_Ready_Expense": "",
        "Apartment_Turnover": "",
        "Redecorating_turnover_expense": "",
        "Total_Make_Ready_Redecorating": "",
        "SUBTOTAL_MAINT_TURNOVER": "",
        "TURNOVER": "",
        "TOTAL_APARTMENT_TURNOVER_COSTS": "",
        "TOTAL_TURNOVER_MAINTENANCE": "",
        "TOTAL_RECONDITIONING": ""
    }
}
Note: The output must be in JSON format. Adherence to this format is mandatory.

                """
                    # Combine the system prompt with the DataFrame prompt
                    full_prompt = f"system\n\n{system_prompt}\nuser\n\n{prompt}\nassistant\n\n"
                    # Initialize the Cohere client
                    api_key = COHERE_API_KEY
                    co = cohere.Client(api_key)

                    response = co.generate(
                        model='command-xlarge-nightly',  # Replace with the correct model ID
                        prompt=full_prompt,
                        max_tokens=1000,
                        temperature=0.5
                    )

                    # Print the generated response
                    print(response.generations[0].text)
                    st.write(response.generations[0].text)
    except Exception as e:
        st.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
