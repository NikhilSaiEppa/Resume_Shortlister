import streamlit as st
import openai
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# OpenAI API setup
client=openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
# Function to send email
def send_email(candidate_name, file_path):
    from_email = "project.use.242@gmail.com"  # Your email
    to_email = "test.purpose.242@gmail.com"  # HR's email

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Candidate Shortlisted: " + candidate_name

    body = "Dear HR,\n\nThe candidate " + candidate_name + " has been shortlisted for the position. Please find the resume attached.\n\nRegards,\nASSISTENCE AI"
    msg.attach(MIMEText(body, 'plain'))

    # Attach resume file
    attachment = open(file_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + file_path)
    msg.attach(part)

    # Connect to SMTP server and send email
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP server and port
    smtp_server.starttls()
    smtp_server.login(from_email, "ameg nfox yvyl audz")  # Your email password
    text = msg.as_string()
    smtp_server.sendmail(from_email, to_email, text)
    smtp_server.quit()

# Function to process uploaded file
def process_uploaded_file(file_path):
    file = client.files.create(
        file=open(file_path, "rb"),
        purpose='assistants'
    )

    file_id = file.id

    assistant = client.beta.assistants.create(
        name="HR Recruiter",
        instructions="Your Task: 'As an HR Recruiter, your task is to indicate whether candidates are selected or not based on the provided job description.' output: 'should be a single word: either 'Selected' or 'Not Selected' no more explanation about resume or candidate'",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo",
        file_ids=[file_id]
    )
    assistant_id = assistant.id

    def read_job_description_from_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()  # Read the content and remove any leading/trailing whitespace
        except FileNotFoundError:
            print("File not found:", file_path)
            return None

    # Specify the file path where your job description is stored
    job_description_file = "job_description.txt"

    # Read the job description from the file
    job_description = read_job_description_from_file(job_description_file)

    messages = [{"role": "user", "content": job_description }]
    thread = client.beta.threads.create(messages=messages)
    thread_id = thread.id

    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    run_id = run.id
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    thread_messages = client.beta.threads.messages.list(thread_id)
    result = thread_messages
    return result

st.title('Application Form')

# Form inputs
name = st.text_input('Name')
phone = st.text_input('Phone Number')
email = st.text_input('Email')
resume = st.file_uploader('Upload Resume', type=['pdf'])

# Submit button
if st.button('Submit'):
    if name and email and resume:
        # Save uploaded file
        with open("resume.pdf", "wb") as f:
            f.write(resume.getbuffer())

        # Process the uploaded file
        result = process_uploaded_file("resume.pdf")
        st.success("Successfully applied")
        a = list(result)
        b = a[0].content[0].text.value
        
        print(b,"b")
        if 'Not Selected' in str(b):
            print("No candidate shortlisted.")
            
        elif 'Selected' in str(b):
            send_email(name, "resume.pdf")
            print("Email sent to HR for shortlisted candidate: " + name)
    else:
        st.error("Please fill in all the fields and upload a resume.")
