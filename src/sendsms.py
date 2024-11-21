import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

def send_sms(body, to):
    account_sid = os.environ["sid"]
    auth_token = os.environ["token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body= body,
        from_="+18557580653",
        to= to,
    )

    print(message.body)