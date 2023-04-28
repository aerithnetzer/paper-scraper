import os
import openai
import pypandoc
import PyPDF2
from PyPDF2 import PdfReader
from PyPDF2 import PdfFileReader, PdfFileWriter

def get_pdf_text(input_file):
    opened_file = open(input_file, 'rb')

# Open the PDF file in read-binary mode
    with opened_file as pdf_file:
    # Create a PyPDF2 PdfFileReader object from the PDF file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Initialize an empty string to store the text content
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
    return text_content

def run_gpt_model(text_content):
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
    instances = []

# Loop through each line of the input string
    for line in lines:
    # Remove the leading "-" character and any whitespace from the line
        instance = line.lstrip('-').strip()

    # Append the instance to the list of instances
        instances.append(instance)

# Return the list of instances
    return instances

def write_file(instances, input_file, output_file):
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
        writer.addMetadata({
            '/Keywords': ', '.join(instances),
        })
    
        # Define the output PDF file
        with open(output_file, 'wb') as out_file:
        # Write the contents of the PdfFileWriter object to the output PDF file
            writer.write(out_file)

def run_pdf_loop(input_path, output_path):
    """Extract keywords from a directory of PDF files using GPT

    Args:
        input_path (str): path to directory of input files
        output_path (str): desired path to directory of output files
    """    

    # Loop through all the files in the "input_path" directory using the os.listdir() method
    for filename in os.listdir(input_path):
        # Check if each file ends with ".pdf"
        if filename.endswith('.pdf'):
            # If it does, set "input_file" as the full path of the current PDF file in the loop
            input_file = os.path.join(input_path, filename)
            
            # Set "output_file" as the full path of where the extracted data from the current PDF file will be saved
            output_file = os.path.join(output_path, filename)

            # Get the text content of the current PDF file using the "get_pdf_text" function 
            text_content = get_pdf_text(input_file)
            
            # Run the GPT model on the text content to generate instances 
            instances = run_gpt_model(text_content)
            
            # Write the instances to the output file and also to the original input file using the "write_file" function
            write_file(instances, input_file, output_file)


def main():  
    input_path = input('input a path to the pdf files you want to tag: ')
    output_path = input('input an output path to put results of the tagging: ')
    run_pdf_loop(input_path, output_path)

main()
