import os
import openai
import PyPDF2
import glob

def process_pdf_file(file_path):
    # Replace this with your own function to process each PDF file
    print(f"Processing {file_path}\n\n")
    
    # Prompt the user to enter the input and output file paths
    input_file = file_path
    output_file = os.path.join(output_directory, os.path.basename(file_path))

    text_content = get_pdf_text(input_file)
    instances = run_gpt_model(text_content)

    write_file(input_file, output_file, instances)

    print(f"{file_path} Done.")


def get_pdf_text(raw_file):
    raw_file = open(raw_file, 'rb')

    # Open the PDF file in read-binary mode
    with raw_file as pdf_file:
        # Create a PyPDF2 PdfFileReader object from the PDF file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Initialize an empty string to store the text content
        text_content = ""

        # Loop through each page of the PDF file
        for page_num in range(pdf_reader.getNumPages()):
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
    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"output some key words to tag this article {text_content}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    outputs = completion.choices[0].text
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

        print(instance)

    return instances


def write_file(input_file, output_file, instances):
    # Open the input PDF file
    with open(input_file, 'rb') as f:
        # Create a PdfFileReader object to read the contents of the PDF file
        reader = PyPDF2.PdfFileReader(f)

        # Get the existing metadata from the PdfFileReader object
        metadata = reader.getDocumentInfo()

        # Create a PdfFileWriter object to write the modified PDF file
        writer = PyPDF2.PdfFileWriter()

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


def main():
    # Replace "/path/to/directory" with the directory path you want to search
    directory_path = '/Users/tnetzer/Desktop/test'
    global output_directory
    output_directory = '/Users/tnetzer/Desktop/output'

    # Use glob to find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(directory_path, "*.pdf"))

    # Loop through each PDF file and call the process_pdf_file function on it
    for pdf_file in pdf_files:
        process_pdf_file(pdf_file)


main()
