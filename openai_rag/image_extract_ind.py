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
    results = {
        image_filename: process_image(os.path.join(image_folder_path, image_filename), queries)
        for image_filename in os.listdir(image_folder_path)
        if image_filename.lower().endswith(('.jpg', '.jpeg', '.png'))
    }
    return results

# Main logic to define queries and call processing functions
if __name__ == "__main__":
    # Define the folder containing images

    #! This works for gzt_images_sub folder
    # image_folder_path = "gzt_images_sub"


    # queries = [
    #     "What is the minister found in this image at the top? Return only the minister found.",
    #     "Return to me a numbered list of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image. If there are none in either column return 'No subjects and functions' or 'No departments, statutory institutions and public corporations' or 'No laws, acts and ordinances to be implemented' respectively.",
    # ]


    #! Check for gzt_images_sub2 folder
    # image_folder_path = "gzt_images_sub2"


    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns
    #     """,
    #     "Return to me a numbered list of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column return 'No subjects and functions' or 'No departments, statutory institutions and public corporations' or 'No laws, acts and ordinances to be implemented' respectively.",
    # ]

    #! Now return as a json object
    # image_folder_path = "gzt_images_sub2"


    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns

    #     Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column leave the list empty for that column.

    #     Return the information as a JSON object, for example:

    #     {
    #         "ministers": 
    #         [
    #             {
    #                 "name": "Minister of Defence",
    #                 "functions": [
    #                     "Ensure national security",
    #                     "Coordinate armed forces",
    #                     "Develop defense policies"
    #                 ],
    #                 "departments": [
    #                     "Office of the Chief of Defence Staff",
    #                     "Sri Lanka Army",
    #                     "Sri Lanka Navy"
    #                 ],
    #                 "laws": [
    #                     "National Security Act No. 45 of 2003",
    #                     "Military Ordinance No. 12 of 1945"
    #                 ]
    #             },
    #         ]
    #     }

    #     """
    # ]

    #! Now return as a text
    image_folder_path = "gzt_images_sub2"


    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns

    #     Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column return (empty) for that column.
    #     Note that each 'subjects and functions' and 'departments, statutory institutions and public corporations' sometimes begin with a number and sometimes do not, do not enumerate the list yourself, make sure you copy the exact number if present. If there is no number before the entry make sure you still include the entry but do not put any number before it.
    #     Also note that each 'laws, acts and ordinances to be implemented' sometimes begin with a bullet point and sometimes do not, make sure you copy the exact format including the same bullet point or not.
        
    #     Return the information as text in the following example format:

    #     # Minister of Defence

    #     Subjects and Functions:
    #     1. Ensure national security
    #     2. Coordinate armed forces

    #     Departments, Statutory Institutions and Public Corporations:
    #     1. Office of the Chief of Defence Staff
    #     2. Sri Lanka Army

    #     Laws, Acts and Ordinances to be Implemented:
    #     - National Security Act No. 45 of 2003
    #     - Military Ordinance No. 12 of 1945

    #     """
    # ]

    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns

    #     Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column return (empty) for that column.
    #     Note that each 'subjects and functions' and 'departments, statutory institutions and public corporations' entry either begin with a number or do not, do not enumerate the list yourself, make sure you copy the exact entry together with the number if there or without the number if not present.
    #     Also note that each 'laws, acts and ordinances to be implemented' either begin with a bullet point or do not, make sure you copy the exact make sure you copy the exact entry together with the bullet point if there or without the bullet point if not present.
    #     If either a number or bullet point is not present ensure you still copy the entry without beginning with either a number or bullet point.
        
    #     Return the information as text in the following example format:

    #     # Minister of Defence

    #     Subjects and Functions:
    #     1. Ensure national security
    #     2. Coordinate armed forces

    #     Departments, Statutory Institutions and Public Corporations:
    #     1. Office of the Chief of Defence Staff
    #     2. Sri Lanka Army

    #     Laws, Acts and Ordinances to be Implemented:
    #     - National Security Act No. 45 of 2003
    #     - Military Ordinance No. 12 of 1945

    #     """
    # ]

    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns

    #     Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column leave the list empty for that column.
    #     NOTE: If a 'subject and functions' or 'departments, statutory institutions and public corporations' entry does not begin with a number in the image, when you return the entry begin with a * (for example 4. * Ensure national security) and if a 'laws, acts and ordinances to be implemented' entry does not begin with a bullet point in the image, when you return the entry begin with a * (for example - * National Security Act No. 45 of 2003).

    #     Return the information as text in the following example format:

    #     # Minister of Defence

    #     Subjects and Functions:
    #     1. Ensure national security
    #     2. * Coordinate armed forces

    #     Departments, Statutory Institutions and Public Corporations:
    #     1. Office of the Chief of Defence Staff
    #     2. Sri Lanka Army

    #     Laws, Acts and Ordinances to be Implemented:
    #     - National Security Act No. 45 of 2003
    #     - * Military Ordinance No. 12 of 1945

    #     """
    # ]

    # queries = [
    #     """
    #     What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
    #     - The minister begins with a number (example 1. Minister of Defence)
    #     - The minister is in the format "Minister of ..."
    #     - The minister is in bold
    #     - The minister is not found inside any table or columns

    #     Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column leave the list empty for that column.
        
    #     STRICT CONDITION: For every *FIRST* entry you are recording in the sections 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' you must follow the following steps:
    #         - Step 1: Check if the entry begins with a number (such as 3. ) or bullet point.
    #         - Step 2: If the entry does not begin with a number or bullet point, add a * before the entry. If the entry does begin with a number or bullet point, do not add a * before the entry.
    #         ** Remember to ONLY follow these instructions for the FIRST entry of each 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' **

    #     Return the information as text in the following example format:

    #     # Minister of Defence

    #     Subjects and Functions:
    #     Ensure national security
    #     Coordinate armed forces

    #     Departments, Statutory Institutions and Public Corporations:
    #     * Office of the Chief of Defence Staff
    #     Sri Lanka Army

    #     Laws, Acts and Ordinances to be Implemented:
    #     * National Security Act No. 45 of 2003
    #     Military Ordinance No. 12 of 1945

    #     """
    # ]

    queries = [
        """
        What are the ministers found in the image? There will always be at least one minister. Use this information to find the minister(s):
        - The minister begins with a number (example 1. Minister of Defence)
        - The minister is in the format "Minister of ..."
        - The minister is in bold
        - The minister is not found inside any table or columns

        Also retrieve lists of the 'subjects and functions', 'departments, statutory institutions and public corporations' and 'laws, acts and ordinances to be implemented' in this image for each minister identified. If there are none in either column leave the list empty for that column.
        
        STRICT CONDITION: Copy each entry exactly as it appears in the column including any numbers or bullet points that may or may appear before it. If a number or bullet point does not appear before an entry do not add one yourself and attempt to enumerate the list by adding additional numbers or bullet points.

        Return the information as text in the following example format:

        # Minister of Defence

        Subjects and Functions:
        4. Ensure national security
        5. Coordinate armed forces

        Departments, Statutory Institutions and Public Corporations:
        Office of the Chief of Defence Staff
        8. Sri Lanka Army

        Laws, Acts and Ordinances to be Implemented:
        1. National Security Act No. 45 of 2003
        2. Military Ordinance No. 12 of 1945

        """
    ]

    # Process all images with the specified queries
    results = process_all_images(image_folder_path, queries)

    # Output the results
    for image, responses in results.items():
        print(f"Results for {image}:")
        for query, response in responses.items():
            # print(f"Query: {query}")
            print(f"Response:\n {response}")
            print("\n" + "="*50 + "\n")
