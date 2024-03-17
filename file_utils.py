import openai_utils as oai
import streamlit as st

def process_uploaded_file(file_path):
    file = oai.client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )

    file_id = file.id

    assistant = oai.client.beta.assistants.create(
        name="HR Recruiter",
        instructions="Your Task: 'As an HR Recruiter, your task is to indicate whether candidates are selected or not based on the provided job description.' output: 'should be a single word: either 'Selected' or 'Not Selected' no more explanation about resume or candidate'",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo",
        file_ids=[file_id]
    )
    assistant_id = assistant.id

    # Specify the file path where your job description is stored
    job_description_file = "job_description.txt"

    # Read the job description from the file
    job_description = oai.read_job_description_from_file(job_description_file)

    messages = [{"role": "user", "content": job_description}]
    thread = oai.client.beta.threads.create(messages=messages)
    thread_id = thread.id

    run = oai.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    run_id = run.id
    while run.status != "completed":
        run = oai.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    thread_messages = oai.client.beta.threads.messages.list(thread_id)
    result = thread_messages
    return result
