import streamlit as st
from email_utils import send_email
from file_utils import process_uploaded_file

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

        print(b, "b")
        if 'Not Selected' in str(b):
            print("No candidate shortlisted.")
        elif 'Selected' in str(b):
            send_email(name, "resume.pdf")
            print("Email sent to HR for shortlisted candidate: " + name)
    else:
        st.error("Please fill in all the fields and upload a resume.")
