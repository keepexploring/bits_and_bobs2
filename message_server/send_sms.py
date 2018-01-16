# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

from_ = ""

def send_sms(message,to):

    message = client.api.account.messages.create(to=to, from_=from_, body=message)

if __name__ == '__main__':

    message="hello"
    to = ""
    send_sms(message, to)
