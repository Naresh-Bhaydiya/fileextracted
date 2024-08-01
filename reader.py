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
                        temperature=0.3
                    )

                    # Print the generated response
                    print(response.generations[0].text)
                    st.write(response.generations[0].text)
    except Exception as e:
        st.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
