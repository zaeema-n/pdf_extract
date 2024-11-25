from openai import OpenAI

def read_text_file(file_path):
    """Read the content of a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_response_to_file(response, file_path):
    """Save the OpenAI response to a text file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response)

def query_openai_with_file(file_path, prompt, client, output_file):
    """Pass file content and a query prompt to OpenAI."""
    # Read the content of the text file
    text_content = read_text_file(file_path)
    
    # Combine the text content with the prompt
    combined_prompt = f"{prompt}\n\n{text_content}"
    
    # Query OpenAI using the client
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Specify the model you'd like to use
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_prompt}
        ]
    )
    
    # Extract the response content
    response_text = response['choices'][0]['message']['content']
    
    # Save response to the output file
    save_response_to_file(response_text, output_file)

# Initialize OpenAI client
client = OpenAI()

# Input and output file paths
input_file_path = "responses.txt"  # Path to your input text file
output_file_path = "csv_response.txt"  # Path to save the output

# Define your query
user_query = """
Convert the provided JSON data into a CSV with two columns: "
"'Minister' and 'Department'. Each minister and their departments should appear as a separate row. "
"Return only the CSV content without extra text or explanations."
"""

# Call the function to process the file and query OpenAI
query_openai_with_file(input_file_path, user_query, client, output_file_path)

print(f"Response saved to {output_file_path}")
