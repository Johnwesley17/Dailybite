import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

def fetch_tech_news():
    url = f"https://newsapi.org/v2/top-headlines?category=technology&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles[:5]  # top 5 articles

def format_news_html(articles):
    html = "<h2>📰 Daily Tech News</h2><ul>"
    for article in articles:
        html += f"""
        <li>
            <a href="{article['url']}" target="_blank"><strong>{article['title']}</strong></a><br/>
            <i>{article['source']['name']}</i><br/>
            <p>{article.get('description', '')}</p>
        </li><br/>
        """
    html += "</ul>"
    return html

def send_email():
    news = fetch_tech_news()
    html_content = format_news_html(news)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📰 DailyByte - Today’s Tech News"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    mime_html = MIMEText(html_content, "html")
    msg.attach(mime_html)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)
