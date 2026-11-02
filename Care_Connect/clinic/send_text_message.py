# account_sid = "AC42429a611898bc2b6883a51a045c0ccc"
# token = "9381505900e31e04ed5b070b8bcb673b"

import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+919496624324",
    from_="+17372508034",
    body="Booked Successfully!",
)

print(message.sid)