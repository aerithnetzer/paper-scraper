def read_key():
    """
    Read in new openAI API key
    """
    import os, stat
    from IPython.display import clear_output

    # Read in new openAI API key, if one exists
    try:
        with open(os.path.expanduser('~/.openaikey.txt'), 'r') as f:
            key = f.readlines()[0]
            return key
    except:
        key = ""

    # Check if API key already exists, skip try-except
    if not key:
        # Prompt user for API key
        try:
            user = str(input())
            clear_output()
            with open(os.path.expanduser('~/.openaikey.txt'), 'w') as keyfile:
                keyfile.write(user)
            os.chmod(os.path.expanduser('~/.openaikey.txt'), stat.S_IREAD | stat.S_IWRITE)
            del user

            with open(os.path.expanduser('~/.openaikey.txt'),'r') as f:
                key = f.readlines()[0]
                return key
            print("Success")
        except:
            print("Something seems wrong with your key")
            


def test_key(api_key):
    import openai
    openai.api_key = api_key

    # create a chat completion
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}])

    # print the chat completion
    print(chat_completion.choices[0].message.content)
    
            
def get_pdf_text(input_file):
    import PyPDF2
    opened_file = open(input_file, 'rb')

# Open the PDF file in read-binary mode
    with opened_file as pdf_file:
    # Create a PyPDF2 PdfFileReader object from the PDF file
        pdf_reader = PyPDF2.PdfFileReader(pdf_file, strict=False)

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

def run_gpt_model(text_content,key):
    import openai
    openai.api_key = key
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [
    {"role": "user", "content" : "output some key words to tag this article " + text_content}]
    )
    #print(completion)
    outputs = completion['choices'][0]['message']['content']
    # print(outputs)
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
        output_data = io.BytesIO()

        # Write the contents of the PdfFileWriter object to the output PDF file
        writer.write(output_data)

        # Write output_data to output_file
        with open(output_file, 'wb') as out_file:
            out_file.write(output_data.getbuffer())

def run_pdf_loop(input_path, output_path, markdown_path):
    """Extract keywords from a directory of PDF files using GPT

    Args:
        input_path (str): path to directory of input files
        output_path (str): desired path to directory of output files
        markdown_paht (str): path to directory of markdown files
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

            # Find markdown documents with the same filenames (use citekeys!)
            try:
                with open(os.path.join(markdown_path,f"{filename[:-4]}.md"),'a') as f:
                    print(f'\n{filename}: {instances}')
                    f.write(", ".join([f"[[{''.join(filter(lambda x: x.isalnum() or x.isspace(), s.strip()))}]]" for s in instances[0].split(',')]))
            except(FileNotFoundError):
                print(f"Could not find corresponding markdown file for {filename[:-4]}.md")
                
def network_graph(keywords,papers,show_singles=False):
    import plotly.graph_objects as go
    import networkx as nx
    from collections import Counter
    edges = []
    for i in range(len(papers[:79])):
        for j in range(len(keywords[i])):
            edges.append([papers[i], keywords[i][j]])

    # Filter the list of paired lists to only include items that appear more than once
    if show_singles:
        # Flatten the list of lists
        flattened = [item for sublist in edges for item in sublist]

        # Count the occurrences of each element in the flattened list
        counts = Counter(flattened)

        # Get all elements that appear more than once
        duplicates = [element for element in counts if counts[element] > 1]
        edges = [edge for edge in edges if edge[0] in duplicates and edge[1] in duplicates]
    
    # Create an empty graph
    G = nx.Graph()

    # Add nodes to the graph
    for sublist in edges:
        for node in sublist:
            G.add_node(node)

    # Add edges to the graph
    for sublist in edges:
        G.add_edge(sublist[0], sublist[1])

    # give a random position to each node
    pos = nx.spring_layout(G)
    for node in G.nodes():
        # print(node)
        # print(pos[nod/e])
        G.nodes[node]['pos'] = pos[node].tolist()
        
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        text=list(G.nodes()),
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        # node_text.append('# of connections: '+str(len(adjacencies[1])))
        node_text.append(list(G.nodes)[node])

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
         layout=go.Layout(
            title='<br>Network graph made with Python',
            titlefont_size=16,
            showlegend=False,
            hovermode='closest',
            template='simple_white',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            )
    fig.show()
    
import os