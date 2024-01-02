Certainly! Below is an updated README that includes the project structure with hidden folders:

---

# Email Sending Script

## Overview

This script is designed to send personalized emails to a list of recipients using Gmail's SMTP server. It reads recipient information from a CSV file, customizes email content based on templates, and sends emails using a rotating set of credentials. The script logs successful and unsuccessful email deliveries.

## Project Structure

```
- EmailSender
    - data
        - email.csv (Hidden)
    - logs (Hidden)
        - error_log.csv (Hidden)
        - sent_emails_log.txt (Hidden)
        - log.txt (Hidden)
        - current_plan.txt (Hidden)
    - templates
        - credentials.json (Hidden)
        - templates.json (Hidden)
        - email_sending_plan.json (made implicitly)
    - email_sender.py
    - plan_manager.py
    - utils.py
```

## Configuration

The script is configured through two JSON files:

1. **credentials.json**: Contains a list of email credentials with email and password (get your app password from [Google Account Security](https://myaccount.google.com/) and generate an app password; also, make sure you have 2-factor authentication enabled).

2. **templates.json**: Contains a list of email templates with subject and body.

3. **email_sending_plan.json**: Contains a list of email sending plans with the number of emails to send per day and creates a 25 day plan for email warmup.

## Usage

1. **Prepare CSV File**: Create a CSV file named `email.csv` with columns, including "Email," "Country," "Tag," and "Name" for recipient information and put it in a `/data` folder.

2. **Set Up Templates**: Customize email templates in the `templates.json` file in `/templates` folder.

3. **Run the Script**: Execute the script by running the main block. Ensure that the necessary files and folders are in place. The script will send emails to recipients specified in the CSV file.

   ```bash
   python email_sender.py
   ```

## Important Notes

- The script uses Gmail's SMTP server. Ensure that "Less secure app access" is enabled for the sender's Gmail account.

- Update the path to your logo file in the script if you want to include a logo in your emails (`'logo.jpg'`).

- Emails are sent in rotation through multiple credentials to avoid exceeding daily sending limits.

- Logs of successful and unsuccessful email deliveries are stored in the `logs` directory.

## Customization

- Modify the `attachments` section to include attachments in your emails.
- Replace placeholders like `[USERNAME]`, `[TAG]`, etc., in email templates with actual data from the CSV file.

## Troubleshooting

- If emails are not being sent, check the error logs (`error_log.csv`) for details on failed deliveries.

- Review the console output for any error messages.

- Ensure that all dependencies are installed and the necessary files are correctly configured.
