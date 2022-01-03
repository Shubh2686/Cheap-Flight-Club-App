import os
import smtplib
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

account_sid = "AC7e2be90f203244355ea771cddc8da87a"
auth_token = "3815c59f184b4783f6db687dd6b01948"

MAIL_PROVIDER = 'smtp.gmail.com'
MAIL = "meditator1305@gmail.com"
PASSWORD = "1305_meditator"

class NotificationManager:

    def send_sms(self, msg):
        client = Client(account_sid, auth_token, http_client=proxy_client)

        message = client.messages \
            .create(
            body=msg,
            from_='+18572675304',
            to='+919460875512'
        )

        print(message.status)

    def send_emails(self, email, msg, link):
        with smtplib.SMTP(MAIL_PROVIDER) as connection:
            connection.starttls()
            connection.login(user=MAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MAIL,
                to_addrs=email,
                msg=f"Subject:New Low Price Flight!\n\n{msg}\n{link}".encode('utf-8')
            )
    pass