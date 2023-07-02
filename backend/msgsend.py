import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
from data import convert_to_formatted_pdf
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

send_email=os.environ['SENDER_EMAIL']
send_password=os.environ['EMAIL_API_PASSWORD']

def send_email(username,receiver_email, responses, fetching_info, embedding_info, sender_email=send_email, sender_password=send_password):
    body = "<html><body>"
    body += "<h1><p>Here is the feedback of the repository:</p></h1>"
    name = responses[0]
    reasons = responses[1]
    body += f"<p><b>Name of the most complex repository:</b> {name}</p>"
    body += f"<p><b>Reasons (BY AI):</b></p>"
    body += f"{reasons}"
    body += "<p><b>Here are some user details:</b></p>"
    if(fetching_info[0] != None and len(fetching_info[0]) > 0):
        body += f"<b>Name:</b>"
        body += f"<p>{fetching_info[0]}</p>"
    if(fetching_info[1] != None and len(fetching_info[1]) > 0):
        body += f"<b>Username:</b>"
        body += f"<p>{fetching_info[1]}</p>"
    if(fetching_info[2] != None and len(fetching_info[2]) > 0):
        body += f"<b>Location:</b>"
        body += f"<p>{fetching_info[2]}</p>"
    if(fetching_info[3] != None and len(fetching_info[3]) > 0):
        body += f"<b>Bio:</b>"
        body += f"<p>{fetching_info[3]}</p>"
    body += f"<p><b>Total time taken to fetch all the codes:</b> {int(fetching_info[-1])} seconds / {int((fetching_info[-1])/60)} min</p>"
    body += f"<p><b>Total time taken to decide the most complex repository by AI:</b> {int(embedding_info[-1])} seconds/ {int((embedding_info[-1])/60)} min</p>"
    body += "<br><br>"
    body += "<p>Thanks,</p>"
    body += "<p>Team GitCrawler</p>"
    body += "</body></html>"

    # Set up the SMTP server
    # Change this if you're using a different email provider
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # Change this if required
    smtp_username = sender_email
    subject = "Github Repository Feedback"

    # Create a multipart message and set the headers
    message = MIMEMultipart()
    # Attach the PDF file
    convert_to_formatted_pdf(username)
    with open(f"pdf_data/api_endpoints_{username}.pdf", "rb") as file:
        attachment = MIMEApplication(file.read(), _subtype="pdf")
    attachment.add_header(
        "Content-Disposition", "attachment", filename=(f"{username}_repositories.pdf")
    )
    message.attach(attachment)
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject + " " + \
        str(datetime.date.today()) + " " + \
        str(datetime.datetime.now().strftime("%H:%M"))

    # Add body to the email as HTML content
    message.attach(MIMEText(body, "html"))

    try:
        # Login to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Cleanup
        server.quit()

        print(f"Email sent successfully to {receiver_email}")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
