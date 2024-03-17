import openai
import os

client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def read_job_description_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Read the content and remove any leading/trailing whitespace
    except FileNotFoundError:
        print("File not found:", file_path)
        return None
