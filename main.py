import schedule
import time
from news_sender import send_email

# Schedule: Every day at 08:00 AM
schedule.every().day.at("14:15").do(send_email)

print("📆 DailyByte Email Scheduler Started...")

while True:
    schedule.run_pending()
    time.sleep(60)




