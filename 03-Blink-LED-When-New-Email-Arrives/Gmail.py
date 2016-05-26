from apiclient import errors
import threading
import time
import RPi.GPIO as GPIO
import GmailAuthorization

PIN = 22
CHECK_INTERVAL = 30

service = None
unread_count = 0


def refresh():
    global unread_count
    try:
        messages = service.users().messages().list(userId='me', q='is:inbox + is:unread').execute()
        unread_count = messages['resultSizeEstimate']
    except errors.HttpError as error:
        print('An error occurred: {0}'.format(error))


def indicator():
    while True:
        if unread_count > 0:
            GPIO.output(PIN, not GPIO.input(PIN))
        else:
            GPIO.output(PIN, GPIO.LOW)
        time.sleep(0.5)


def monitor():
    while True:
        refresh()
        time.sleep(CHECK_INTERVAL)


def start_indicator():
    t = threading.Thread(target=indicator)
    t.daemon = True
    t.start()


def start_monitor():
    t = threading.Thread(target=monitor)
    t.daemon = True
    t.start()


def load_service():
    global service
    service = GmailAuthorization.get_service()


def start():
    load_service()
    start_indicator()
    start_monitor()
