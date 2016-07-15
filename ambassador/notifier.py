#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Send email notifications."""

import os
import datetime
import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    """Send email notificatations through SMTP"""
    if 'SMTP_PASS' in os.environ:
        time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        msg = MIMEText(body.format(time))

        msg['Subject'] = subject
        msg['From'] = os.environ['SMTP_FROM']
        msg['To'] = os.environ['SMTP_TO']

        # Login credentials to sendgrid
        username = os.environ['SMTP_USER']
        password = os.environ['SMTP_PASS']

        # Open a connection to the SendGrid mail server
        smtp = smtplib.SMTP(os.environ['SMTP_HOST'])

        # Authenticate
        smtp.login(username, password)

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())
        smtp.quit()

class Notifier(object):
    """Notifier class"""

    def __init__(self):
        self._live = False

    def api_is_up(self):
        """Notify API up"""
        if self._live is False:
            send_email("CGC API status", "TI went UP at {}")
        self._live = True

    def api_is_down(self):
        """Notify API down"""
        if self._live is True:
            send_email("CGC API status", "TI went DOWN at {}")
        self._live = False
