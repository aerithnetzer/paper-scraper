import os
import openai
import pypandoc
import PyPDF2
from PyPDF2 import PdfReader
from PyPDF2 import PdfFileReader, PdfFileWriter


def get_pdf_text():
    opened_file = open(input_file, 'rb')

# Open the PDF file in read-binary mode
    with opened_file as pdf_file:
    # Create a PyPDF2 PdfFileReader object from the PDF file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Initialize an empty string to store the text content
        global text_content
        text_content = ""

    # Loop through each page of the PDF file
        for page_num in range(1): # range(pdf_reader.getNumPages()):
        # Get the current page object
            page_obj = pdf_reader.getPage(page_num)

        # Extract the text content from the page
            page_text = page_obj.extractText()

        # Append the text content from the page to the overall string
            text_content += page_text

    # Print the final text content string
    print(text_content)
    run_gpt_model()

def run_gpt_model():
    openai.api_key = os.environ["OPENAI_API_KEY"]
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [
    {"role": "user", "content" : "output some key words to tag this article " + text_content}]
    )
    #print(completion)
    outputs = completion['choices'][0]['message']['content']
    print(outputs)
    # Split the input string into lines
    lines = outputs.splitlines()

# Initialize an empty list to store the instances
    global instances
    instances = []

# Loop through each line of the input string
    for line in lines:
    # Remove the leading "-" character and any whitespace from the line
        instance = line.lstrip('-').strip()

    # Append the instance to the list of instances
        instances.append(instance)

# Print the list of instances
    print(instances)
    write_file()

def write_file():
    # Open the input PDF file
    with open(input_file, 'rb') as f:
    # Create a PdfFileReader object to read the contents of the PDF file
        reader = PdfFileReader(f)
    
    # Get the existing metadata from the PdfFileReader object
        metadata = reader.getDocumentInfo()
    
    # Create a PdfFileWriter object to write the modified PDF file
        writer = PdfFileWriter()
    
    # Loop through each page of the input PDF file
        for i in range(reader.getNumPages()):
        # Get the current page from the PdfFileReader object
            page = reader.getPage(i)
        
        # Add the current page to the PdfFileWriter object
            writer.addPage(page)
    
    # Add your custom metadata properties here:
        instances
        writer.addMetadata({
            '/Keywords': ', '.join(instances),
        })
    
        # Define the output PDF file
        with open(output_file, 'wb') as out_file:
        # Write the contents of the PdfFileWriter object to the output PDF file
            writer.write(out_file)

def main():
    global input_file
    global output_file
    input_file = input('input a path to the pdf file you want to tag: ')
    output_file = input('input an output path to put results of the tagging: ')
    get_pdf_text()

main()