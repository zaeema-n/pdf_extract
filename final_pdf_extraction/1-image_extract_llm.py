# This script is used to extract the text from the images in the folder 'gzt_images' using OpenAI LLM
# and save the extracted text in a text file 'int_ministers_department_json.txt' in json format.

import base64
import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

# Function to encode an image in base64
def encode_image(image_path):
    """Encodes an image file in base64 format."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send a query to the AI model with an image
def query_image(image_base64, query):
    """Sends a query along with the base64-encoded image to the AI model and returns the response."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

# Function to process an image file with a list of queries
def process_image(image_path, queries):
    """Processes a single image file by sending a series of queries and returns a dictionary of responses."""
    base64_image = encode_image(image_path)
    responses = {query: query_image(base64_image, query) for query in queries}
    return responses

# Function to process all images in a folder with a list of queries
def process_all_images(image_folder_path, queries):
    """Processes all images in the specified folder with the given list of queries."""
    # Sort images lexicographically by filename
    image_filenames = sorted(
        [f for f in os.listdir(image_folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    )

    # Process each image in the sorted order
    results = {}
    for image_filename in image_filenames:
        print(f"Processing file: {image_filename}\n")  # Print the current file being processed
        results[image_filename] = process_image(os.path.join(image_folder_path, image_filename), queries)
    return results

# Main logic to define queries and call processing functions
if __name__ == "__main__":

    #! Now return as a json object
    image_folder_path = "gzt_images"


    queries = [
        """
        What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
        - The minister begins with a number (example 1. Minister of Defence)
        - The minister is in the format "Minister of ..."
        - The minister is in bold
        - The minister is not found inside any table or columns

        Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column leave the list empty for that column.

        Return the information as a JSON object, for example:

        {
            "ministers": 
            [
                {
                    "name": "Minister of Defence",
                    "functions": [
                        "Ensure national security",
                        "Coordinate armed forces",
                        "Develop defense policies"
                    ],
                    "departments": [
                        "Office of the Chief of Defence Staff",
                        "Sri Lanka Army",
                        "Sri Lanka Navy"
                    ],
                    "laws": [
                        "National Security Act No. 45 of 2003",
                        "Military Ordinance No. 12 of 1945"
                    ]
                },
            ]
        }

        Don't add any extra text such as ```json so that i can directly save the response to a json file.

        """
    ]

    with open('int_ministers_department_json.txt', 'w', encoding='utf-8') as file:
        # Process all images with the specified queries
        results = process_all_images(image_folder_path, queries)

        # Output the results to the file
        for image, responses in results.items():
            for query, response in responses.items():
                file.write(f"{response}\n\n")  # Write the response followed by a new line
