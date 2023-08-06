## GITHUB_REPOSITORY_COMPLEXITY_ANALYSER

--------------
A Python-based tool that aims to identify the most technically complex and challenging repository from a GitHub user's profile. The tool functions by taking a GitHub user's URL as input and then utilizes the power of GPT (Generative Pre-trained Transformer) and LangChain. The process involves assessing each repository individually to determine its technical complexity.

## Backend Logic

--------------
The tool follows a unique approach inspired by how we interact with AI language models. First, the code is sent in chunks to GPT, prompting it to keep track and memorize all the provided chunks. Once all chunks are processed, the last prompt was sent, instructing GPT to read the entire code in those chunks. In response, GPT provides a complexity score as the first line of its response, followed by a detailed explanation of the reasons for its assessment in the second line.

The main logic of backend is to send the code in 'chunks'. There were total 'n+1' prompts sent, where 'n' is the total chunks in which the code is broken. The prompts that are sent with all chunks are used to calculate its complexity reason and is different from the final prompt that carries no chunk. The final prompt is sent to tell GPT that all chunks have been received and Now you have to calculate the reason of code complexity. Also GPT summarises the reasons for all chunks' complexity and finally LangChain is used to calculate the score based on that summarised reason. 

- `app/`: Contains the web application code.
  - `templates/`: Holds the HTML templates for the user interface.
  - `__init__.py`: Initializes the Flask application and defines routes.


- `utils/`: Holds utility functions or modules used in the project.
  - `backend.py`: For getting API data from Github, Preprocessing and returning most complex repository with reason
  - `gpt.py`: Functions for interacting with GPT and generating score and reason.

- `main.py`: The entry point of the application. Contains the main Flask application and routes for handling user requests.

- `README.md`: The documentation file explaining the project, its file structure, and instructions for running and deploying.

## Usage

To use this project, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Install the dependencies.
3. Configure the necessary API keys and settings in the appropriate files.
4. Run the application: `python main.py`
5. Access the tool in your browser at `http://localhost:5000` (or the specified port).


