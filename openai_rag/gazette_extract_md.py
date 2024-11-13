#import pdfplumber
from openai import OpenAI

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def save_response_to_text_file(response, file_name):
    with open(file_name, 'w') as file:
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

# Extract text from the PDF
#pdf_text = extract_text_from_pdf("gzt.pdf")

# Example usage with different prompts
query1 = """
Find all the ministers in the following document: 

Note that I want them as a list separated by new lines.
Format should look like this:

Minister of Defence
Minister of Finance, Economic Development, Policy formulation, Planning and Tourism
Minister of Energy
Minister of Agriculture, Lands, Livestock, Irrigation, Fisheries and Aquatic Resources

Don't include any other text. Only the list of ministers.

"""
# query_openai_with_prompt(pdf_text, query1, client, "ministers_response_v5.txt")

query2 = """
In the document for each minister, there is a list of `Departments, Statutory Institutions and Public Corporations` that they are responsible for.

Note that I want them as a list separated by new lines. 

We need to create a separate section for each minister in the response. 
To get this information you only need to read the column 2 of the table.
And you can identify the department as it starts with a number.

Also note that there content for each minister can be in multiple pages. 
So note that you need to get the content for each minister from multiple pages if it is necessary.

Use the following format:

Minister 
--------

List the `Departments, Statutory Institutions and Public Corporations` line by line.

"""

query3 = """
For each minister, locate the table where their assigned departments, statutory institutions, and public corporations are listed in column 2. Each section for a minister may span multiple pages, so continue extracting until you reach the next minister’s section.

Ensure you focus only on column 2 of each table, and ignore any other columns. Specifically, look for entries in column 2 that start with a number, as these indicate the departments, statutory institutions, or public corporations.

Use the following format for each minister:

Minister
--------

List each `Department, Statutory Institution, or Public Corporation` on a new line as they appear in column 2.

If content for a minister spans multiple pages, continue appending from column 2 until all relevant entries for that minister are captured.
"""

query4 = """
For each minister, locate the table listing their assigned Departments, Statutory Institutions, and Public Corporations in column 2 only. Ignore all entries from column 3, which usually contain legal acts, laws, or ordinances, often identified by terms such as "Act," "Law," "Ordinance," or "Regulation."

Each section for a minister may span multiple pages, so continue extracting until reaching the next minister’s section. Extract only those entries in column 2 that start with a number, and ensure that any entry with the terms "Act," "Law," "Ordinance," or "Regulation" is excluded.

Use the following format for each minister:

Minister
--------

List each `Department, Statutory Institution, or Public Corporation` in column 2 on a new line as they appear.

Examples:
- Include entries like "1. Office of the Chief of Defence Staff" or "2. Sri Lanka Army" from column 2.
- Exclude entries like "Sri Lanka Disaster Management Act No. 13 of 2005," "Public Security Ordinance," or similar items from column 3.
"""

query5 = """
Extract the list of **Departments, Statutory Institutions, and Public Corporations** under the responsibility of each minister from the document. Each entry for a minister is found in **column 2 of the tables** and starts with a number.

**Key Instructions**:

- Only extract entries from **column 2**. Ignore all other columns.
- Entries in column 2 **begin with a number**, which indicates a department, statutory institution, or public corporation.
- **Exclude any items** that include terms like **"Act," "Law," "Ordinance," or "Regulation,"** as these typically appear in other columns and are not departments or institutions.
- For each minister, list the departments, institutions, or corporations in order, starting a new line for each entry.
- Continue collecting entries for each minister until reaching the section for the next minister. If a minister’s entries span multiple pages, ensure you capture all relevant entries across pages.

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
Extract the list of **Departments, Statutory Institutions, and Public Corporations** under the responsibility of each minister from the document. Each entry for a minister is found in **column 2 of the tables** and starts with a number.
"""

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

# Example usage
markdown_content = read_markdown_file("gzt.md")
# print(markdown_content)

query_openai_with_prompt(markdown_content, query6, client, "ministers_response_v5.txt")
