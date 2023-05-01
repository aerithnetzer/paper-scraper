# paper-scraper
## What this code currently does

This project currently inputs the first page page of a PDF, runs the text through the GPT-3.5-Turbo, and then returns a PDF with metadata tagged in the 'Keywords' field.

## How to use this code

1. Save a PDF file to your computer
2. When running main.py, the program will prompt you for the file path of the PDF you would like to tag (TODO Edit this section)
3. It will then prompt you for an output file path for the GPT model to run though
4. When you open the output file, it will have metadata tagged in the 'Keywords' field

## What I want this code to do in the future

1. Put the output keywords in obsidian
2. Get citation information from input pdfs

## Architecture for next feature:

1. Rip metadata/citation information form the pdf
2. Create Markdown file with same file name as PDF (for example: bunny.pdf -> bunny.md)
3. Paste citation information + keywords as tag + metadata in markdown for each file

EXAMPLE:

filename: bunny.md
