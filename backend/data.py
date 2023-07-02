import json
import os
from github import Github
from fpdf import FPDF
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# This is the acess key of the person who will use this code. Note that this has usage limit and needs to be reset if the limit is reached.
# Also I have set expiration date of 30 days.
github_access_key = os.environ['GITHUB_ACCESS_TOKEN']

def fetch_github(username):
    # Initialize an empty list to hold the user information.
    userinfo=[]
    # Replace 'YOUR_ACCESS_TOKEN' with your personal access token
    access_token = github_access_key
    # Create a Github instance with the access token
    g = Github(access_token)
    # Get a user by username
    user = g.get_user(username)
    userinfo.append(user.name)
    userinfo.append(user.login)
    userinfo.append(user.location)
    userinfo.append(user.bio)
    # List repositories of the user
    repositories = user.get_repos()
    count = 0
    # Create an empty repsonse object where we will store the results
    response = {}
    print("Getting all the information online..................................................")
    # Start the timer
    start_time = time.time()
    for repo in repositories:
        repository = g.get_repo(f'{username}/{repo.name}')
        count += 1
        if count >= 15:
            break
        try:
            repo_data = {}
            traverse_repository(repository, repo_data, 0)
            if repo_data:
                response[repo.name] = repo_data
        except Exception as e:
            print(e)
    end_time = time.time()
    # Check if the JSON file exists
    json_file_path = f"json_data/repository_codes_{username}.json"
    if not os.path.exists(json_file_path):
        # Create the file if it doesn't exist
        open(json_file_path, "w").close()

    # Save response as JSON
    with open(json_file_path, "w") as json_file:
        json.dump(response, json_file, indent=4)
    userinfo.append(end_time-start_time)
    return userinfo

        
'''A helper function that traverse the repository. Even if there are folders and nested files the function would traverse each  of them recursively to find the code bases.'''
# In this code I have kept the number of files to be traversed to be 5 only to keep it short and simple. Otherwise it will take good amount of time to traverse the entire repository.
def traverse_repository(repository, repo_data, count, path=""):
    IGNORED_FOLDERS=["node_modules", "vs", "venv"]
    contents = repository.get_contents(path)
    files_traversed = 0  # Track the number of files traversed
    should_exit = False  # Flag to determine when to exit the function
    while contents:
        # Condition to break the loop and eventually the function itself. If you want all the files then remove this line of codes.
        if files_traversed >= 5 or count >= 5:
            should_exit = True  # Set the flag to exit the function
            break
        file_content = contents.pop(0)
        if file_content.type == "dir":
            if file_content.name in IGNORED_FOLDERS:
                continue  # Ignore the directory and continue to the next iteration
            files_traversed += 1
            traverse_repository(repository, repo_data,
                                count+1, file_content.path)
        else:
            files_traversed += 1
            file_extension = file_content.path.split(".")[-1]
            if file_extension in ["txt", "py", "ipynb", "md", "html", "htm", "css", "jsx", "js", 'sol', 'cpp', "kt", "tsx", "ts", "go", "php", "sol","java"]:
                file_name = file_content.path.split("/")[-1]
                file_data = {
                    "code": file_content.decoded_content.decode("utf-8")
                }
                repo_data[file_name] = file_data
                tt = file_content.decoded_content.decode("utf-8")
                print(f"{file_name} *************************************")
                print(f"{tt}")
                # Increment the count of files traversed
    if should_exit:
        return


def convert_to_pdf(username):
    print("Converting into PDFs............................................")
    # Read the JSON data from the file
    with open(f'json_data/repository_codes_{username}.json', 'r') as file:
        data = json.load(file)
    # Create a PDF document
    pdf = FPDF()
    # Set up the document
    pdf.set_title('API Endpoints Documentation')
    pdf.set_auto_page_break(auto=True, margin=15)
    # Add a cover page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, 'API Endpoints Documentation', ln=True, align='C')
    # Iterate over the JSON data and add repository name and files with code to the PDF
    pdf.set_font('Arial', 'B', 16)
    for repository, files in data.items():
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        # Handle Unicode characters in repository name
        repository = repository.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, f'Repository: {repository}', ln=True, align='L')
        pdf.set_font('Arial', '', 12)
        for filename, content in files.items():
            pdf.multi_cell(0, 10, f'File: {filename}')
            pdf.set_font('Courier', '', 10)
            # Handle Unicode characters in code content
            code = content['code'].encode(
                'latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, code)
    # Save the PDF document with UTF-8 encoding
    pdf.output(f'pdf_data/api_endpoints_{username}.pdf', 'F')


def convert_to_formatted_pdf(username):
    print("Converting into PDFs............................................")
    # Read the JSON data from the file
    with open(f'json_data/repository_codes_{username}.json', 'r') as file:
        data = json.load(file)
    # Create a PDF document
    pdf = FPDF()
    # Set up the document
    pdf.set_title('Repository Codes')
    pdf.set_auto_page_break(auto=True, margin=15)
    # Add a cover page
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 20, 'Repository Codes', ln=True, align='C')
    # Iterate over the JSON data and add repository name and files with code to the PDF
    pdf.set_font('Arial', 'B', 16)
    for repository, files in data.items():
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        # Handle Unicode characters in repository name
        repository = repository.encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, f'Repository: {repository}', ln=True, align='L')
        pdf.set_font('Arial', '', 12)
        for filename, content in files.items():
            pdf.multi_cell(10, 10, '') 
            pdf.multi_cell(0, 10, f'File: {filename}', 'B')
            pdf.set_font('Courier', '', 10)
            # Handle Unicode characters in code content
            code = content['code'].encode('latin-1', 'replace').decode('latin-1')
            code_lines = code.split('\n')
            for line in code_lines:
                line = line.strip()  # Remove unnecessary spaces from the beginning and end of the line
                pdf.multi_cell(0, 5, line)  # Adjust the line spacing to make it more compact
    # Save the PDF document with UTF-8 encoding
    pdf.output(f'pdf_data/api_endpoints_{username}.pdf', 'F')


