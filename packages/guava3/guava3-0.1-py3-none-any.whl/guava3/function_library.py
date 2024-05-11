import sys
import io
import ast
import subprocess
import re
import datetime
import matplotlib
import base64
matplotlib.use('Agg')  # Set a non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
import os
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output
import requests
from guava3.utils import count_tokens


def end(*args, **kwargs):
    return "THE END"

shell = InteractiveShell()

def python_run(chat_history: list) -> str:
    """
    Execute a python code
    """

    # Override matplotlib's show method
    def show_plot_as_base64():
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        sys.stdout.write(f'\n```\n![Image](data:image/png;base64,{img_data})\n```\n')
        sys.stdout.flush()
        buffer.close()
        
    plt.show = show_plot_as_base64

    # Save current directory
    current_dir = os.getcwd()
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # Change current dir
    code_str = chat_history[-1][1]
    os.makedirs("resources/local_data", exist_ok=True)
    os.chdir("resources/local_data")

    # Run code
    with capture_output() as captured:
        shell.run_cell(code_str)

    # Change to original dir
    os.chdir(current_dir)

    output = '\n'.join([captured.stdout,captured.stderr])

    # Use regular expression to remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)

    if output == '\n':
        output = 'Run successful\n'
    
    # Check if the output isn't too long
    if count_tokens(re.sub(r'!\[Image\]\([^)]+\)','',output))>5000:
        output = "Returned value is too long. Try displaying something shorter"

    output = f"Python Output:\n```\n{output.strip()}\n```"
    output = output.replace("```\n```", "")

    return output

def python_run_backend(chat_history: list) -> str:
    """
    Execute a python code
    """

    code_str = chat_history[-1][1]

    # Post a request to the ipython API
    captured = requests.post('http://127.0.0.1:8000/run_code/', json={'code_str': code_str}).json()
    
    output = '\n'.join([captured['stdout'],captured['stderr']])

    # Use regular expression to remove ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    output = ansi_escape.sub('', output)

    if output == '\n':
        output = 'Run successful\n'
    
    # Check if the output isn't too long
    if count_tokens(output)>5000:
        output = "Returned value is too long. Try displaying something shorter"

    output = f"Python Output:\n```\n{output}```"
    output = output.replace("```\n```", "")
    
    return output

def python_run_old(chat_history: list) -> str:
    """
    Execute a python code
    """

    # Save current directory
    current_dir = os.getcwd()
    
    # Change to the target directory
    os.chdir('local_data')

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    code_str = chat_history[-1][1]

    # Remove empty lines from the end of the code string
    code_str = code_str.rstrip()

    # Split the code string into lines
    code_lines = code_str.strip().split('\n')
    
    # Separate the code into statements and the final expression/line
    statements, final_line = code_lines[:-1], code_lines[-1]
    
    # Create a new output stream to capture printed values
    new_output = io.StringIO()
    
    # Save the original output stream
    original_output = sys.stdout
    
    # Redirect the standard output to our new stream
    sys.stdout = new_output
    
    returned_output = None
    
    try:
        # Check for indentation in the final line and valid syntax
        is_indented = final_line.startswith(('    ', '\t'))
        is_valid_syntax = True
        try:
            ast.parse(final_line)
        except SyntaxError:
            is_valid_syntax = False

        # Override matplotlib's show method
        def custom_show(*args, **kwargs):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"plot_{timestamp}.png"
            plt.savefig(filename)
            print(f"```\n![Image]({filename})\n\n```")
            plt.close()
        
        plt.show = custom_show
        
        # If not indented and valid syntax, exec statements and eval final line
        if not is_indented and is_valid_syntax:
            if statements:  # check if there are statements to exec
                exec('\n'.join(statements), globals())
            try:
                returned_output = eval(final_line, globals())
            except SyntaxError:
                returned_output = exec(final_line, globals())
        else:
            exec(code_str, globals())
    except Exception as e:
        # In case of an exception, store the error message as the returned output
        returned_output = f"{type(e).__name__}: {str(e)}"
    finally:
        # Always ensure that the standard output is reset to the original
        sys.stdout = original_output
    os.chdir(current_dir)
    
    # Get the string value from our new output stream
    printed_output = new_output.getvalue()
    
    # Close the new output stream
    new_output.close()

    printed_output = str(printed_output)
    if returned_output is None:
        returned_output = ''
    else:
        returned_output = str(returned_output) + "\n"
    
    # Return both the printed and returned output
    output = printed_output + returned_output

    if output == '':
        output = 'Run successful'

    output = f"```\n{output}```"
    output = output.replace("```\n```", "")
    
    return f"Python Output:\n"+output    



def save_markdown(chat_history):
    md_string = chat_history[-1][1]
    with open('output.md', 'w', encoding='utf-8') as file:
        file.write(md_string)
    return 'File sucessfully saved to "output.md"'

def chat_error(chat_history):
    return "Attention: You have to either run a python code or rewrite the previous message and send back to the user."

def chat_error_for_all(chat_history):
    last_speaker = chat_history[-1][1][:4]
    return f"{last_speaker}: Error: You have to either run a python code or rewrite the previous message and send back to the user."

def install_libraries(chat_history):
    libraries_string = chat_history[-1][1]
    libraries = [lib.strip() for lib in libraries_string.split(',')]
    
    logs = []

    for library in libraries:
        try:
            subprocess.check_call(['pip', 'install', library])
            logs.append(f'Successfully installed {library}')
        except subprocess.CalledProcessError:
            logs.append(f'Error installing {library}')

    return '\n'.join(logs)

def run_terminal(chat_history):
    command = chat_history[-1][1]
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
    


def search_metadata(chat_history: list) -> str:
    """
    Search for database metadata in a Parquet file based on keywords provided in the chat history.
    If matches are found, they are displayed first, followed by the rest of the content. 
    If no matches are found, display the entire content of the Parquet file.
    The Parquet file is located at a fixed path.
    """
    # Define o caminho fixo para o arquivo Parquet
    file_path = './db_metadata.parquet'

    # Tenta carregar os metadados do banco de dados do arquivo Parquet
    try:
        db_metadata = pd.read_parquet(file_path)
    except Exception as e:
        return f"Error loading Parquet file: {str(e)}"

    # Prepara um filtro inicial falso
    filter_condition = pd.Series([False] * len(db_metadata))

    for subject in chat_history:
        # Converte o termo para string para evitar TypeError
        subject_str = str(subject)

        # Atualiza a condição de filtro para incluir linhas que correspondam ao termo atual
        filter_condition |= (
            db_metadata['table_name'].str.contains(subject_str, case=False, na=False) |
            db_metadata['column_name'].str.contains(subject_str, case=False, na=False) |
            db_metadata['description'].str.contains(subject_str, case=False, na=False)
        )

    # Separa os dados filtrados e os não filtrados
    filtered_metadata = db_metadata[filter_condition]
    non_filtered_metadata = db_metadata[~filter_condition]

    # Concatena os resultados filtrados com os não filtrados, se houver correspondências
    if not filtered_metadata.empty:
        final_metadata = pd.concat([filtered_metadata, non_filtered_metadata])
    else:
        final_metadata = db_metadata

    # Verifica se foram encontrados resultados
    if final_metadata.empty:
        return "The metadata file is empty."

    # Prepara a saída formatada
    output = io.StringIO()
    final_metadata.to_csv(output, index=False)
    result = output.getvalue()
    output.close()

    return f"```\n{result}\n```"


def reset_globals(preserved_vars, initial_globals):
    current_globals = set(globals().keys())
    to_delete = current_globals - preserved_vars - initial_globals
    for var in to_delete:
        del globals()[var]



FUNCTION_MAP = {name: obj for name, obj in globals().items() if callable(obj) and not name.startswith("_")}





