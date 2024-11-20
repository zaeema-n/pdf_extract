import openai
import os
import csv

# Initialize the OpenAI client
client = openai.OpenAI()

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure the environment variable is set

# Function to read JSON data from the txt file
def read_json_from_txt(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        return file.read()

# Function to request OpenAI to generate CSV formatted data
def generate_csv_from_openai(input_text):
    # Send the prompt to OpenAI to generate CSV output without quotes
    response = client.Completion.create(
        engine="gpt-4",  # Or gpt-3.5 if you prefer
        prompt=f"""
        Given the following data, extract the 'minister' names and their 'departments' and return the output in CSV format with two columns:
        Minister Name, Department
        
        Data:
        {input_text}
        
        The CSV should contain the minister names and corresponding department names without any quotation marks. Please return the result in CSV format, like:
        Minister of Trade, Commerce, Food Security, Co-operative Development, Industry and Entrepreneurship Development, Sri Lanka Institute of Textile and Apparels
        """,
        max_tokens=1500,
        temperature=0.3
    )
    
    return response.choices[0].text.strip()

# Function to save the generated CSV to a file with proper handling of commas
def save_csv(csv_data, output_filename):
    # Write the CSV data to a file, ensuring that commas in fields are escaped correctly
    with open(output_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        # Split each line from the response by newline to create a row
        for line in csv_data.splitlines():
            writer.writerow(line.split(','))  # Split by commas and write each row

# Input filename (responses.txt)
input_filename = 'responses.txt'

# Read the content from the txt file
input_text = read_json_from_txt(input_filename)

# Request OpenAI to generate CSV data
csv_output = generate_csv_from_openai(input_text)

# Specify the output CSV file name
output_filename = 'ministers_departments.csv'

# Save the CSV data to a file
save_csv(csv_output, output_filename)

print("CSV file has been saved successfully.")
