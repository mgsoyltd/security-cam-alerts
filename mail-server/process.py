from sys import argv
import os
from detect import detect_people
from store import insertAlert, convertToBinaryData, write_log
from datetime import datetime
from time import sleep

if __name__ == '__main__':

    if len(argv) < 4:
        print("Invalid arguments")
        exit()

    tempfile = argv[1]
    subject = argv[2]
    timestamp = datetime.strptime(argv[3], "%Y%m%d%H%M%S")

    try:
        if detect_people(tempfile, file=True):
            # Found - write to the detect table
            data = convertToBinaryData(tempfile)
            insertAlert(subject, timestamp, data, True)
            write_log("Detection successfully stored to database")
    except Exception as err:
        write_log("Detection failed", err)
    finally:
        for i in range(10):
            try:
                write_log("Deleting temp file", tempfile)
                os.unlink(tempfile)
                break
            except Exception as err:
                write_log("Tempfile deletion failed", err)
                sleep(1)
                continue
