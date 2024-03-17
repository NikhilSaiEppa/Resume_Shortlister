import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(candidate_name, file_path):
    from_email = "Your_email@gmail.com"  # Your email
    to_email = "Hr's_email@gmail.com"  # HR's email

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
    smtp_server.login(from_email, "Your_app_password")  # Your email password
    text = msg.as_string()
    smtp_server.sendmail(from_email, to_email, text)
    smtp_server.quit()
