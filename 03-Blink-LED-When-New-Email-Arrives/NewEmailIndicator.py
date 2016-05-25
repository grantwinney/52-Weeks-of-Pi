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

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

# Number of seconds to wait before checking for mail again
CHECK_MAIL_INTERVAL = 5


# Initialize GPIO settings
def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([22, 32, 36], GPIO.OUT)
    #GPIO.setup(12, GPIO.IN)
    #GPIO.add_event_detect(12, GPIO.BOTH, callback=


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


gmail_unread_count = 0


def gmail_led_blink():
    while True:
        if gmail_unread_count > 0:
            GPIO.output(22, not GPIO.input(22))
        else:
            GPIO.output(22, GPIO.LOW)
        time.sleep(0.5)


# Use Gmail API to check for new mail, every CHECK_MAIL_INTERVAL seconds
def check_gmail(service):
    global gmail_unread_count

    t = threading.Thread(target=gmail_led_blink)
    t.daemon = True
    t.start()

    while True:
        try:
            messages = service.users().messages().list(userId='me',q='is:inbox + is:unread').execute()
            gmail_unread_count = messages['resultSizeEstimate']
        except errors.HttpError as error:
            print('An error occurred: {0}'.format(error))

        time.sleep(CHECK_MAIL_INTERVAL)


def initialize_gmail_check(service):
    t = threading.Thread(target=check_gmail, args=(service,))
    t.daemon = True
    t.start()


def main():
    credentials = get_gmail_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    try:
        initialize_gpio()
        initialize_gmail_check(service)
        message = raw_input("\nPress any key to exit.\n")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
