# /usr/bin/env python
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import Client

# Find these values at https://twilio.com/user/account
account_sid = "ACa561bc741453b2b5a94a91e3ba5c3237"
auth_token = "50f13d34604ddb1ec442b48292938e7c"
client = Client(account_sid, auth_token)

from_ = "+441412807832"

def send_sms(message,to):

    message = client.api.account.messages.create(to=to, from_=from_, body=message)

if __name__ == '__main__':

    message="hello"
    to = "+447892882181"
    send_sms(message, to)
