import base64
import os
from openai import OpenAI

client = OpenAI()

# Function to encode an image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Directory containing all images
# image_folder = "gzt_images"

query4 = """
For each minister, locate the table listing their assigned Departments, Statutory Institutions, and Public Corporations in column 2 only. Ignore all entries from column 3, which usually contain legal acts, laws, or ordinances, often identified by terms such as "Act," "Law," "Ordinance," or "Regulation."

Each section for a minister may span multiple images, so continue extracting until reaching the next minister’s section. Extract only those entries in column 2 that start with a number, and ensure that any entry with the terms "Act," "Law," "Ordinance," or "Regulation" is excluded.

Use the following format for each minister:

Minister
--------

List each `Department, Statutory Institution, or Public Corporation` in column 2 on a new line as they appear.

Examples:
- Include entries like "1. Office of the Chief of Defence Staff" or "2. Sri Lanka Army" from column 2.
- Exclude entries like "Sri Lanka Disaster Management Act No. 13 of 2005," "Public Security Ordinance," or similar items from column 3.
"""

query5 = """
Each image has a minister at the top beginning with a number (eg 1. Minister of Defence), and below that, there is a table with three columns.
The ministers can run across multiple images, and each minister's table can also run across multiple images.
Extract the list of **Departments, Statutory Institutions, and Public Corporations** under the responsibility of each minister from the second column in the table in the images. Each entry for a minister is found in **column 2 of the tables** and starts with a number.

**Key Instructions**:

- Only extract entries from **column 2**. Ignore all other columns.
- Entries in column 2 **begin with a number**, which indicates a department, statutory institution, or public corporation.
- It is possible that in some images the second column does not contain entries, in this instance **do not extract anything** from the image.
- **Exclude any items** that include terms like **"Act," "Law," "Ordinance," or "Regulation,"** as these typically appear in other columns and are not departments or institutions.

- For each minister, list the departments, institutions, or corporations in order, starting a new line for each entry.
- Continue collecting entries for each minister until reaching the section for the next minister. If a minister’s entries span multiple images, ensure you capture all relevant entries across images. But **only** capture information from the second column always.
- Do not get information from the first column or third column, only retrieve from the second column.
- Extract the exact wordings from the second column only, do not translate anything and do not change the wordings, spellings or summarize anything.
- Even if you go to a new image remember to still **only** extract information from the second column, **not** the first column and **not** the third column.

**Format**:

For each minister, use this structure:

Minister of [Title]
--------

1. [First Department/Institution]
2. [Second Department/Institution]
...

**Example**:

Minister of Defence
--------

1. Office of the Chief of Defence Staff
2. Sri Lanka Army
3. Sri Lanka Navy
...

Make sure only the entries from column 2 are listed, with no legal references or acts included in the output.
"""


query6 = """
Each image has a minister at the top beginning with a number (eg 1. Minister of Defence), and below that, there is a table with three columns.
The ministers can run across multiple images, and each minister's table can also run across multiple images.
Extract the list of **Departments, Statutory Institutions, and Public Corporations** under the responsibility of each minister from the second column in the table in the images. Each entry for a minister is found in **column 2 of the tables** and starts with a number.

**Key Instructions**:

- Only extract entries from **column II** under Departments, Statutory Institutions, and Public Corporations. Ignore all other columns.
- Entries in column II under Departments, Statutory Institutions, and Public Corporations **begin with a number**, which indicates a department, statutory institution, or public corporation.
- It is possible that in some images the second column, Column II, under Departments, Statutory Institutions, and Public Corporations does not contain entries, in this instance **do not extract anything** from the image.
- **Exclude any items** that include terms like **"Act," "Law," "Ordinance," or "Regulation,"** as these typically appear in other columns and are not departments or institutions.

- For each minister, list the departments, institutions, or corporations in order, starting a new line for each entry.
- Continue collecting entries for each minister until reaching the section for the next minister. If a minister’s entries span multiple images, ensure you capture all relevant entries across images. But **only** capture information from the second column, column II under Departments, Statutory Institutions, and Public Corporations always.
- Do not get information from the first column, column I, under Subjects and Functions or third column, Column III under laws, acts and ordinances to be implemented, only retrieve from the second column, column II.
- Extract the exact wordings from the second column, Column II only, do not translate anything and do not change the wordings, spellings or summarize anything.
- Even if you go to a new image remember to still **only** extract information from the second column, column II, **not** the first column, column I and **not** the third column, column III.

**Format**:

For each minister, use this structure:

Minister of [Title]
--------

1. [First Department/Institution]
2. [Second Department/Institution]
...

**Example**:

Minister of Defence
--------

1. Office of the Chief of Defence Staff
2. Sri Lanka Army
3. Sri Lanka Navy
...

Make sure only the entries from column 2, Column II are listed, with no legal references or acts included in the output.
"""

query7 = """
Each image has a minister at the top beginning with a number (eg 1. Minister of Defence), and below that, there is a table with three columns.
The ministers can run across multiple images, and each minister's table can also run across multiple images.
Extract the list of **Departments, Statutory Institutions, and Public Corporations** under the responsibility of each minister from under **Column II** in the table in the images. Each entry for a minister is found in **column II of the tables** and starts with a number.

**Key Instructions**:

- Only extract entries from the column **Column II** under Departments, Statutory Institutions, and Public Corporations. Ignore all other columns.
- Entries in the column Column II **begin with a number**, which indicates a department, statutory institution, or public corporation.
- It is possible that in some images, the column Column II, does not contain entries, in this instance **do not extract anything** from the image.
- **Exclude any items** that include terms like **"Act," "Law," "Ordinance," or "Regulation,"** as these typically appear in other columns and are not departments or institutions.

- For each minister, list the departments, institutions, or corporations in order, starting a new line for each entry.
- Continue collecting entries for each minister until reaching the section for the next minister. If a minister’s entries span multiple images, ensure you capture all relevant entries across images. But **only** capture information from the column Column II under Departments, Statutory Institutions, and Public Corporations always.
- Do not get information from the first column, column I, under Subjects and Functions or third column, Column III under laws, acts and ordinances to be implemented, only retrieve from the second column, column II.
- Extract the exact wordings from Column II only, do not translate anything and do not change the wordings, spellings or summarize anything.
- Even if you go to a new image remember to still **only** extract information from the column Column II, **not** Column I and **not** Column III.

**Format**:

For each minister, use this structure:

Minister of [Title]
--------

1. [First Department/Institution]
2. [Second Department/Institution]
...

**Example**:

Minister of Defence
--------

1. Office of the Chief of Defence Staff
2. Sri Lanka Army
3. Sri Lanka Navy
...

Make sure only the entries from column 2, Column II are listed, with no legal references or acts included in the output.
"""

query8 = """
Each image has a minister at the top beginning with a number (eg 1. Minister of Defence), and below that, there is a table with three columns.

The ministers can run across multiple images, and each minister's table can also run across multiple images.

For every unique minister throughout the images list down all the entities found in Column II of the table for each minister. In some images, Column II may not have naything under it, in such cases do not extract anything from the image.

Return the entitites for each minister as a numbered list.

Whenever you are extracting from a new image, check that you are currently in Column II, then check if there is anything under "Column II". If there is nothing under Column II, ignore the image and do not extract anything from it, otherwise only extract everything from within Column II.
"""

query9 = """
I have given you a series of images, follow these step-by-step instructions for each image:

Step 1 - At the top of the image there is a minister's name, check if this is the current minister you are extracting from. If it is a new minister, start a new numbered list for the new minister.
Step 2 - Below the minister's name there is a table with three columns.
Step 3 - Look for the column "Column II" in the table, this is the only column you should be extracting from.
Step 4 - If there are no entries inside the column "Column II" in the image, do not extract **anything** from the image, completely ignore all information in this image and move on to the next image. If there is content inside "Column II", extract all the content from "Column II" and append it to the numbered list under the current minister.
Step 5 - Continue this process for all the images provided.

"""

query10 = """
I have given you a series of images, follow these step-by-step instructions for each image:

Step 1 - At the top of the image there is a minister's name, check if this is the current minister you are extracting from. If it is a new minister, start a new numbered list for the new minister.
Step 2 - Below the minister's name there is a table with three columns. Each column has a heading at the top of the column which is the name of the column.
Step 3 - Look for the column named "Column II" in the table, this is the column you should be extracting from. Do not extract anything from the columns named "Column I" or "Column III"
Step 4 - If there are no entries inside the column named "Column II" in the image, do not extract **anything** from the image, completely ignore all information in this image and move on to the next image. If there is content inside "Column II", extract all the content from "Column II" and append it to the numbered list under the current minister.
Only extract content from inside "Column II", do not pay attention to the meaning of the content.
Step 5 - Continue this process for all the images provided.

"""

query11 = """
Task Instructions:

Identify the Minister: At the top of each image, there will be a minister's name. Check if this minister matches the last minister you were extracting information from.
- If this is the same minister as in the previous image, continue appending to their list.
- If this is a new minister, start a new list specifically for this minister.
- Locate the Table and Columns: Directly below the minister’s name, there is a table with three columns. Find the column labeled "Column II" within this table.

Check for Content in Column II:
- If "Column II" is empty, do not extract anything from this image. Simply move on to the next image.
- If "Column II" has content, proceed with extraction.

Extract and Append Content:
- Extract all text from "Column II" and add each entry to the numbered list for the current minister.
- Continue appending any additional content found in subsequent images under the same minister, until a new minister appears.
- Repeat for All Images: Follow this process for each image, ensuring that content from "Column II" is only extracted and appended when it is not empty, and that each minister’s list is clearly separated.

Output Format:
For each minister:
- Begin with the minister's name as a heading.
- List each item from "Column II" in order, as it appears, under a numbered list for that minister.
"""

# Path to your image
image_folder_path = "gzt_images_sub"

# Initialize the messages list
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query9,
            },
        ],
    }
]

# Loop through all files in the folder
for image_filename in os.listdir(image_folder_path):
    # Check if the file is an image (you can refine this condition based on your image types)
    if image_filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_folder_path, image_filename)
        base64_image = encode_image(image_path)

        # Add the image as a part of the message
        messages[0]['content'].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            },
        })

# print(messages)

# Sending the request with multiple images
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

# Print the response for each image
print(response.choices[0].message.content)
