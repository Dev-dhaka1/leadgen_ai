# import os
# import re
# import csv
# import smtplib
# from datetime import datetime
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from crewai.tools import tool


# def clean_text(content: str) -> str:
#     """Strip any HTML tags, SVG, and extra whitespace from content."""
#     # Remove SVG blocks
#     content = re.sub(r'<svg[\s\S]*?</svg>', '', content)
#     # Remove HTML tags
#     content = re.sub(r'<[^>]+>', '', content)
#     # Remove form blocks
#     content = re.sub(r'<form[\s\S]*?</form>', '', content)
#     # Clean up excessive whitespace
#     content = re.sub(r'\n{3,}', '\n\n', content)
#     content = re.sub(r'[ \t]+', ' ', content)
#     return content.strip()


# def get_data_dir() -> str:
#     """Get the data directory path and create it if missing."""
#     data_dir = os.path.join(os.path.dirname(__file__), "data")
#     os.makedirs(data_dir, exist_ok=True)
#     return data_dir


# @tool("Email Saver Tool")
# def email_tool(content: str) -> str:
#     """Save the generated lead outreach emails to a plain text file in the data folder."""
#     data_dir = get_data_dir()
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"leads_outreach_{timestamp}.txt"
#     filepath = os.path.join(data_dir, filename)

#     clean_content = clean_text(content)

#     try:
#         with open(filepath, "w", encoding="utf-8") as f:
#             f.write(clean_content)
#         return f"✅ Outreach saved to: data/{filename}"
#     except Exception as e:
#         return f"❌ Failed to save file: {str(e)}"


# @tool("Email Sender Tool")
# def send_email_tool(
#     to_email: str,
#     subject: str,
#     body: str,
#     prospect_name: str = "",
#     company: str = ""
# ) -> str:
#     """Send a plain text cold email to a prospect via SMTP and log it to CSV."""

#     # Validate email address
#     if not to_email or "@" not in to_email:
#         return f"❌ Invalid email address: '{to_email}' — skipping."

#     smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
#     smtp_port = int(os.getenv("SMTP_PORT", "587"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_pass = os.getenv("SMTP_PASS")

#     if not smtp_user or not smtp_pass:
#         return "❌ Error: SMTP_USER or SMTP_PASS not set in .env"

#     # Clean body before sending
#     clean_body = clean_text(body)

#     try:
#         msg = MIMEMultipart("alternative")
#         msg["Subject"] = subject
#         msg["From"] = smtp_user
#         msg["To"] = to_email
#         msg.attach(MIMEText(clean_body, "plain"))

#         with smtplib.SMTP(smtp_host, smtp_port) as server:
#             server.ehlo()
#             server.starttls()
#             server.login(smtp_user, smtp_pass)
#             server.sendmail(smtp_user, to_email, msg.as_string())

#         status = "sent"
#         result_msg = f"✅ Email sent to {to_email}"

#     except smtplib.SMTPException as e:
#         status = "failed"
#         result_msg = f"❌ Failed to send to {to_email}: {str(e)}"

#     # Always log to CSV regardless of send success/failure
#     _log_to_csv(
#         company=company,
#         prospect_name=prospect_name,
#         to_email=to_email,
#         subject=subject,
#         body=clean_body,
#         status=status
#     )

#     return result_msg


# def _log_to_csv(company, prospect_name, to_email, subject, body, status):
#     """Internal function to log every email attempt to CSV."""
#     data_dir = get_data_dir()
#     csv_path = os.path.join(data_dir, "sent_emails_log.csv")

#     file_exists = os.path.isfile(csv_path)

#     try:
#         with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
#             fieldnames = [
#                 "timestamp", "company", "prospect_name",
#                 "to_email", "subject", "body", "status"
#             ]
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             if not file_exists:
#                 writer.writeheader()

#             writer.writerow({
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "company": company,
#                 "prospect_name": prospect_name,
#                 "to_email": to_email,
#                 "subject": subject,
#                 "body": body,
#                 "status": status,
#             })
#     except Exception as e:
#         print(f"⚠️ CSV logging failed: {str(e)}")


import os
import re
import csv
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai.tools import tool


def clean_text(content: str) -> str:
    content = re.sub(r'<svg[\s\S]*?</svg>', '', content)
    content = re.sub(r'<[^>]+>', '', content)
    content = re.sub(r'<form[\s\S]*?</form>', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    return content.strip()


def get_data_dir() -> str:
    # Walk up from this file to find the data folder reliably
    current = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current, "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


@tool("Email Saver Tool")
def email_tool(content: str) -> str:
    """Save the generated lead outreach emails to a plain text file in the data folder."""
    data_dir = get_data_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"leads_outreach_{timestamp}.txt"
    filepath = os.path.join(data_dir, filename)

    clean_content = clean_text(content)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_content)
        return f"✅ Outreach saved successfully to: data/{filename}"
    except Exception as e:
        return f"❌ Failed to save: {str(e)}"


@tool("Email Sender Tool")
def send_email_tool(
    to_email: str,
    subject: str,
    body: str,
    prospect_name: str = "",
    company: str = ""
) -> str:
    """Send a plain text cold email to a prospect and log it to CSV."""

    if not to_email or "@" not in to_email:
        return f"❌ Invalid email address: '{to_email}' — skipping."

    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    if not smtp_user or not smtp_pass:
        return "❌ SMTP credentials missing in .env"

    clean_body = clean_text(body)

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg.attach(MIMEText(clean_body, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, to_email, msg.as_string())

        status = "sent"
        result_msg = f"✅ Email sent to {to_email}"

    except Exception as e:
        status = f"failed ({str(e)})"
        result_msg = f"❌ Failed: {str(e)}"

    _log_to_csv(company, prospect_name, to_email, subject, clean_body, status)
    return result_msg


def _log_to_csv(company, prospect_name, to_email, subject, body, status):
    data_dir = get_data_dir()
    csv_path = os.path.join(data_dir, "sent_emails_log.csv")
    file_exists = os.path.isfile(csv_path)

    try:
        with open(csv_path, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "timestamp", "company", "prospect_name",
                "to_email", "subject", "body", "status"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "company": company,
                "prospect_name": prospect_name,
                "to_email": to_email,
                "subject": subject,
                "body": body,
                "status": status,
            })
    except Exception as e:
        print(f"⚠️ CSV log failed: {str(e)}")