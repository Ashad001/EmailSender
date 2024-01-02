import os
import pandas as pd
import ssl
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import random
import time
import json

from plan_manager import PlanManager
from utils import generate_email_sending_plan, save_to_json

class EmailManager:
    def __init__(
        self,
        credentials_file_path="./templates/credentials.json",
        templates_file_path="./templates/templates.json",
        log_file="./logs/sent_emails_log.txt",
    ):
        self.credentials_file_path = credentials_file_path
        self.templates_file_path = templates_file_path
        self.log_file = log_file
        self.credentials = []
        self.templates = []
        self.current_credential_index = 0
        self.load_credentials()
        self.load_templates()
        
        pm = PlanManager("./logs/current_plan.txt")
        print(pm.current_number)    
        self.curr_day = pm.current_number
        pm.increment_number_for_new_day()
            
        if not os.path.exists("./templates/email_sending_plan.json"):
            total_days = 25
            initial_emails_to_send = 1
            increment_range = (2, 4)
            output_filename = "./templates/email_sending_plan.json"

            email_plan = generate_email_sending_plan(total_days, initial_emails_to_send, increment_range)
            save_to_json(email_plan, output_filename)

            print(f"Email sending plan generated and saved to {output_filename}")
        
        with open('./templates/email_sending_plan.json') as f:
            email_sending_plan = json.load(f)

        self.day_plan = email_sending_plan['email_sending_plan'][str(self.curr_day)]['emails']
        
    def load_credentials(self):
        with open(self.credentials_file_path, "r") as credentials_file:
            credentials_data = json.load(credentials_file)
            self.credentials = credentials_data.get("credentials")

    def load_templates(self):
        with open(self.templates_file_path, "r") as templates_file:
            templates_data = json.load(templates_file)
            self.templates = templates_data.get("templates")

    def get_current_credential(self):
        return self.credentials[self.current_credential_index]

    def switch_to_next_credential(self):
        self.current_credential_index = (self.current_credential_index + 1) % len(
            self.credentials
        )

    def send_email(
        self, receiver_email, subject, message, image_path=None, attachment_path=None
    ):
        current_credential = self.get_current_credential()
        smtp_server = "smtp.gmail.com"
        smtp_port = 465

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = current_credential["email"]
        msg["To"] = receiver_email
        msg.attach(MIMEText(message, "html"))

        if image_path:
            image = MIMEImage(open(image_path, "rb").read())
            image.add_header("Content-ID", "<logo>")
            msg.attach(image)

        if attachment_path:
            with open(attachment_path, "rb") as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(attachment_path),
                )
                msg.attach(pdf_attachment)

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, context=context)
        server.login(current_credential["email"], current_credential["password"])
        server.sendmail(current_credential["email"], receiver_email, msg.as_string())
        server.quit()

    def update_log(self, data):
        with open(self.log_file, "a") as log:
            log.write(data + "\n")

    def read_log(self):
        try:
            with open(self.log_file, "r") as log:
                data = log.read().splitlines()
            return data
        except FileNotFoundError:
            return []


if __name__ == "__main__":
    emails_file_path = "./data/email.csv"
    templates_file_path = "./templates/templates.json"

    if not os.path.exists("./logs"):
        os.mkdir("./logs")

    error_file = "./logs/error_log.csv"
    all_logs = "./logs/log.txt"
    sent_logs = "./logs/sent_emails_log.txt"

    emails_per_credential = (
        1  # Increase this number if you want to send more emails per credential
    )

    if not os.path.exists(emails_file_path):
        print(
            'Please create a csv file with the name "email.csv" and add the emails to send to in the "Email" column.'
        )
        exit()

    emails_dataframe = pd.read_csv(emails_file_path, on_bad_lines="warn")
    if "Email" not in emails_dataframe.columns:
        print('Please add the emails to send to in the "Email" column of the csv file.')
        exit()

    email_manager = EmailManager(templates_file_path=templates_file_path)
    row_num = 0
    email_sends_max = random.randint(email_manager.day_plan['min'], email_manager.day_plan['max'])
    email_sends_max *= len(email_manager.credentials)
    email_sends_count = 0
    
    print(email_sends_max)
    flag = False
    for _ in range((len(emails_dataframe) // emails_per_credential) + 1):
        for _ in range(emails_per_credential):
            if email_sends_count >= email_sends_max:
                flag = True
                continue
            if emails_dataframe.empty:
                break
            if row_num >= len(emails_dataframe):
                break
            row = emails_dataframe.to_dict(orient="records")[row_num]
            country = row["Country"]
            tag = row["Tag"]
            name = row["Name"]
            receiver_email = row["Email"]
            row_num += 1
            selected_template = random.choice(email_manager.templates)

            subject = selected_template["subject"]
            subject = subject.replace("[USERNAME]", name)
            subject = subject.replace("[TAG]", tag)
            # Replace other tags with their values here

            message = selected_template["body"]
            message = message.replace("[USERNAME]", name)
            message = message.replace("[TAG]", tag)
            # Replace other tags with their values here

            # attachment_path = "path/to/your/attachment.pdf"

            if receiver_email in email_manager.read_log():
                print(f"Email already sent to: {receiver_email}")
                with open(all_logs, "+a") as f:
                    f.write(f"Email already sent to: {receiver_email}\n")
                continue

            try:
                email_manager.send_email(
                    receiver_email,
                    subject,
                    message,
                    image_path=None,
                    attachment_path=None,
                )  # Add images and attachments here: 
                print(
                    f'Email sent successfully to: {receiver_email} using {email_manager.get_current_credential()["email"]}'
                )
                email_sends_count += 1

                time.sleep(random.randint(5, 8))
                email_manager.update_log(f"{receiver_email}")

                with open(all_logs, "+a") as f:
                    f.write(
                        f"Email sent to {receiver_email} using {email_manager.get_current_credential()['email']}\n"
                    )

            except Exception as e:
                print((f"Error when sending mail to: {receiver_email}\n"))
                with open(all_logs, "+a") as f:
                    f.write(f"Error when sending mail to: {receiver_email}\n")
                with open(error_file, "a") as error_log:
                    error_log.write(f"{country},{tag},{name},{receiver_email}\n")
        
        if flag:
            break
        email_manager.switch_to_next_credential()
