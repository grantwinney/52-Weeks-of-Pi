from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import threading
import time
import RPi.GPIO as GPIO

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

# Board pins
GMAIL_PIN = 22
YAHOO_PIN = 32
MSOFT_PIN = 36
CHECK_NOW_PIN = 12

# Number of seconds to wait before checking for mail again
CHECK_GMAIL_INTERVAL = 30

gmail_service = None
gmail_unread_count = 0


# Initialize GPIO settings
def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([GMAIL_PIN, YAHOO_PIN, MSOFT_PIN], GPIO.OUT)
    GPIO.setup(CHECK_NOW_PIN, GPIO.IN)
    GPIO.add_event_detect(CHECK_NOW_PIN, GPIO.RISING, callback=check_mail_accounts_now, bouncetime=1000)


def check_mail_accounts_now(_channel):
    check_gmail_now()


# Get valid user credentials from storage or complete OAuth2 flow to revalidate
def get_gmail_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to {0}'.format(credential_path))
    return credentials


def gmail_led_blink():
    while True:
        if gmail_unread_count > 0:
            GPIO.output(GMAIL_PIN, not GPIO.input(GMAIL_PIN))
        else:
            GPIO.output(GMAIL_PIN, GPIO.LOW)
        time.sleep(0.5)


# Use Gmail API to check for new mail, every CHECK_MAIL_INTERVAL seconds
def check_gmail():
    global gmail_unread_count

    t = threading.Thread(target=gmail_led_blink)
    t.daemon = True
    t.start()

    while True:
        check_gmail_now()
        time.sleep(CHECK_GMAIL_INTERVAL)


def check_gmail_now():
    global gmail_unread_count
    try:
        messages = gmail_service.users().messages().list(userId='me',q='is:inbox + is:unread').execute()
        gmail_unread_count = messages['resultSizeEstimate']
    except errors.HttpError as error:
        print('An error occurred: {0}'.format(error))


def initialize_gmail_check():
    t = threading.Thread(target=check_gmail)
    t.daemon = True
    t.start()


def main():
    global gmail_service

    credentials = get_gmail_credentials()
    http = credentials.authorize(httplib2.Http())
    gmail_service = discovery.build('gmail', 'v1', http=http)

    try:
        initialize_gpio()
        initialize_gmail_check()
        message = raw_input("\nPress any key to exit.\n")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
