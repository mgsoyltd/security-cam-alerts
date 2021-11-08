#!python3

import os
from datetime import datetime
from time import sleep
import asyncore
from smtpd import SMTPServer
import email
from store import StoreData, write_log
from decouple import config


URL = config('URL')
PORT = config('PORT', cast=int)
DEST_DIR = config('DEST_DIR')


class EmlServer(SMTPServer):
    no = 0

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        timestamp = datetime.now().replace(microsecond=0)
        # White email to temporary file
        tempfile = 'email/%s.eml' % (timestamp)
        write_log(tempfile)
        with open(tempfile, 'wb') as fb:
            fb.write(data)

        # msg = MIMEApplication(data)
        # attachments = msg.get_payload()

        msg = email.message_from_file(open(tempfile))
        attachments = msg.get_payload()

        if os.path.isfile(tempfile):
            os.remove(tempfile)

        try:
            subject = str(msg).split("Your IPCamera:", 1)[1].split("\n", 1)[0]
        except Exception as err:
            try:
                subject = str(msg).split("Subject: ", 1)[1].split("\n", 1)[0]
            except Exception as err2:
                subject = "Unknown"

        write_log("Subject:", subject)

        for attachment in attachments:
            try:
                file = attachment.get_filename()
                if file == None:
                    continue
                write_log("Attachment:", file)
                filename = os.path.join(DEST_DIR, file)
                mgsdata = attachment.get_payload(decode=True)

                # Trigger DB storing and people detection in the image
                StoreData(mgsdata, filename, 'db', subject,
                          timestamp, True).process()                

            except Exception as err:
                # write_log(err)
                pass


def run():
    retries = 30
    while retries > 0:
        try:
            EmlServer((URL, PORT), None)
            print("Email server is listening at %s:%d" % (URL, PORT))
            asyncore.loop()
            break
        except Exception:
            sleep(1)
            retries -= 1
            continue
        except KeyboardInterrupt:
            print("\nUser cancelled.")
            break


if __name__ == '__main__':
    run()
