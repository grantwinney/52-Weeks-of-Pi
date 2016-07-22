# Blink LED When New Email Arrives
Authenticates to your Gmail account, then polls your unread message account via their API every xx seconds. When unread mail arrives, an LED blinks. When you mark it read, the LED turns off.

There are two files of interest:

* GmailAuthorization.py contains the code for authorizing to Gmail so you can check for email. I had this in a separate file because I was originally planning on connecting to multiple services. Learning one API was enough fun for me though, so if you want to connect to Yahoo or whatever Microsoft is calling their service these days, you'll have to check out their docs. :)

* Gmail.py contains the code for checking for email, after you've authorized yourself.

## To Run

Run the NewEmailIndicator.py file.
