#!/usr/bin/env python
# coding: utf-8

import re
import requests
import nbconvert
import tiktoken
import yaml
from langchain.langchain import LangChain

# Function to read the exclude configuration from the YAML file
def read_exclude_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

# Load the exclude configuration from the config file
exclude_config = read_exclude_config('exclude_config.yaml')
skip_files_extensions = exclude_config.get('skip_files_extensions', [])
skip_files_patterns = exclude_config.get('skip_files_patterns', [])

def repository_complexity_evaluation(github_url):
    url = f"https://api.github.com/users/{github_url}/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repositories = response.json()
    else:
        repositories = None
    if repositories is None:
        print(" no repo to evaluate")
        return
    max_complexity_score=0
    most_complex_reason=''
    most_complex_repo= None

    for repo in repositories:
        repo_name = repo['name']

        # Fetch files for the repository
        files_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        files_response = requests.get(files_url)
        files = files_response.json()

        # Combine code from all files into a single string
        combined_code = ''
        for file in files:
            file_path = file['path']
            file_name = file['name']

            # Exclude certain file types or directories if needed
            if file_path.endswith(tuple(skip_files_extensions)) or any(file_path.startswith(pattern) for pattern in skip_files_patterns):
                continue

            # Get the download URL
            download_url = file['download_url']
            try:
                code_response = requests.get(download_url)
                file_content = code_response.content.decode('utf-8')
                # Check if the file is a Jupyter notebook
                if download_url.endswith('.ipynb'):
                    # Convert Jupyter notebook to Python code using nbconvert
                    python_code = nbconvert.PythonExporter().from_notebook_node(nbconvert.reads(file_content, nbconvert.NO_CONVERT)).strip()
                    code = python_code['code']
                else:
                    code = file_content
                # Remove comments
                code = re.sub(r"#.*", "", code)
                # Remove blank lines
                code = "\n".join(line for line in code.splitlines() if line.strip())
                combined_code += code  # Combine code from all files
            except requests.exceptions.RequestException:
                continue

        # Preprocess combined code into chunks
        all_chunks = convert_to_chunk(combined_code, 3700)

        # Process all the chunks and get the cumulative score and reason
        score = 0
        cumulative_reason = ''
        total_chunks = len(all_chunks)

        for i, chunk in enumerate(all_chunks, 1):
            # Generate the prompt for the current chunk
            prompt = f'You are a code complexity analyser, and you are given a code that comes to you in {total_chunks} chunks. You have to memorise all chunks and When you receive the last chunk of code, all you have to do is to determine the complexity of the entire code with reason.\n\n'
            prompt += f'Total Chunks: {total_chunks}\nCurrent Chunk: {i}\n\n'
            prompt += f'{chunk.strip()}\nCONTINUED IN NEXT MESSAGE...\n'

            # Get the reason for the current chunk
            _, reason = generate_gpt_response(prompt)

            # Accumulate cumulative reason
            cumulative_reason += f'Chunk {i}/{total_chunks}:\n{reason}\n\n'

        # The final chunk is received, now send a prompt for the entire code
        final_prompt = f'You are a code complexity analyser, and you have to determine the complexity of the provided code.\n\n'
        final_prompt += f'You are provided with {total_chunks} chunks of code above, and now you have to give the complexity score out of 10 and reason of the complexity of the above code which was sent to you in {total_chunks} chunks.\n\n'
        final_prompt += f'You must also summarise this cumulative reason {cumulative_reason} you have povided for the {total_chunks} chunks individually to make the final reason. You should send the response such that it has score in first line and reason in second line.\n'

        # Get the score and reason for the entire code
        score, reason = generate_gpt_response(final_prompt)
        complexity_score=calculate_complexity_score(reason)
        # Update the most complex repository
        if complexity_score > max_complexity_score:
            max_complexity_score = complexity_score
            most_complex_repo = repo_name
            most_complex_reason = reason

    return most_complex_repo, max_complexity_score, most_complex_reason


def convert_to_chunk(code, max_chunk_length=3000):
    lines = code.splitlines()
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

    all_chunks = []
    current_chunk = ""
    encoded_lines = str(encoding).splitlines()
    for line in encoded_lines:
        # Check if adding the line to the current chunk exceeds the maximum length
        if len(current_chunk) + len(line) < max_chunk_length:
            current_chunk += line + '\n'
        else:
            # If the current chunk exceeds the maximum length, add it to the list of chunks
            all_chunks.append(current_chunk)
            # Start a new chunk with the current line
            current_chunk = line + '\n'

    # Add the last chunk to the list of chunks
    all_chunks.append(current_chunk)

    return all_chunks

