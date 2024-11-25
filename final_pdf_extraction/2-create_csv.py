# This file uses OpenAI LLM to convert the json data to a csv file

from openai import OpenAI
import csv

def save_response_to_text_file(response, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response)

def query_openai_with_prompt(pdf_text, prompt, client, file_name):
    # Send text to OpenAI API using streaming
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"{prompt}\n\n{pdf_text}"}],
        stream=True,
    )
    # Collect the response
    response_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_text += chunk.choices[0].delta.content

    # Save the entire response to a text file
    save_response_to_text_file(response_text, file_name)


client = OpenAI()

query1 = """
Convert the provided JSON data into a CSV with two columns: "
"'Minister' and 'Department'. Each minister and their departments should appear as a separate row. "
"Return only the CSV content without extra text or explanations."
"Do not include anything like ```csv."
"Use appropriate escaping for special characters, such as wrapping entries including commas in double quotes."
"STRICT CONDITION: Do not include a header row."
"""

def read_text_file(file_path):
    """Read the content of a text file and return it as a variable."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

text_content = read_text_file("int_ministers_department_json.txt") 

query_openai_with_prompt(text_content, query1, client, "int_ministers_departments_csv.txt")

def txt_to_csv(txt_file_path, csv_file_path):
    """Convert a .txt file (formatted like CSV) to a .csv file."""
    
    # Open the .txt file and read its content
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        # Read the lines from the text file
        lines = txt_file.readlines()
    
    # Open the .csv file for writing
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write each line to the CSV
        for line in lines:
            # Remove any extra whitespace and split by commas (because entries are comma-separated)
            columns = line.strip().split('","')
            
            # Remove the surrounding quotes from each column
            columns = [col.strip('"') for col in columns]
            
            # Write the cleaned columns to the .csv file
            csv_writer.writerow(columns)

txt_to_csv("int_ministers_departments_csv.txt", "ministers_departments.csv")