import os
import json
import smtplib
import schedule
import time
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from campaign_parser import initialize_state, load_state, update_state, get_today_offset
from campaign_state import load_campaign

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load campaign data
campaign = load_campaign("campaign.json")
initialize_state(start_date=datetime.today().strftime("%Y-%m-%d"), email_series=campaign["email_series"])
def generate_prompt(stage, campaign):
    features_text = ", ".join(campaign["features"])
    prompt = (
        f"You are a marketing copywriter.\n"
        f"Write an engaging email for the product '{campaign['product_name']}' aimed at '{campaign['target_audience']}'.\n"
        f"Theme: {stage['theme']}\n"
        f"Objective: {stage['objective']}\n"
        f"Features: {features_text}\n"
        f"The email should be informative, persuasive, and concise.\n"
    )
    return prompt


def parse_gemini_response(response_text):
    try:
        # Clean response if Gemini adds explanation text
        json_start = response_text.find('{')
        json_str = response_text[json_start:]
        content_dict = json.loads(json_str)
        
        subject = content_dict.get("subject", "No Subject")
        body = content_dict.get("body", "No Body")
        cta = content_dict.get("cta", "No CTA")
        return subject, body, cta
    except json.JSONDecodeError:
        print("❌ Failed to parse Gemini response as JSON.")
        return "No Subject", "No Body", "No CTA"

def format_email(subject, body, cta):
    plain_text = f"{body}\n\n{cta}"
    html_content = f"""
    <html>
      <body>
        <p>{body}</p>
        <p><strong>{cta}</strong></p>
      </body>
    </html>
    """
    return plain_text, html_content

def generate_and_send_email():
    today_offset = get_today_offset()

    stage = next((s for s in campaign["email_series"] if s["day_offset"] == today_offset), None)
    if not stage:
        print(f"📅 No email scheduled for today (offset: {today_offset})")
        return

    state = load_state()
    if today_offset in state["sent_emails"]:
        print(f"✅ Email for offset {today_offset} already sent.")
        return

    prompt = generate_prompt(stage, campaign)
    response = model.generate_content(prompt)
    subject, body, cta = parse_gemini_response(response.text)
    plain_text, html_content = format_email(subject, body, cta)

    for recipient in campaign["recipients"]:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = recipient
        msg.set_content(plain_text)
        msg.add_alternative(html_content, subtype='html')

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
                print(f"✅ Email sent to {recipient} for day offset {today_offset}")
        except Exception as e:
            print(f"❌ Failed to send email to {recipient}: {e}")

    update_state(today_offset)

# Schedule the job to run every day at 09:00 AM
schedule.every().day.at("09:00").do(generate_and_send_email)

print("⏳ Scheduler is running... Press Ctrl+C to stop.")
generate_and_send_email()  # Run immediately for testing
while True:
    schedule.run_pending()
    time.sleep(60)

