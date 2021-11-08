from sys import argv
import os
from detect import detect_people
from store import insertAlert, convertToBinaryData, write_log
from datetime import datetime
from time import sleep
from pathlib import Path

def deleteFiles(pattern):
    delfiles = [f for f in Path(folder).glob(pattern) if f.is_file()]
    for file in delfiles:
        write_log("Deleting temp file", file)
        try:
            os.unlink(file)
        except Exception as err:
            write_log("Error deleting file", err)

if __name__ == '__main__':

    if len(argv) < 2:
        print("Invalid arguments")
        exit()

    # Folder to poll files
    folder = argv[1]
    write_log("Serving files in folder", folder)

    # Serve forever
    while True:
        sleep(1)

        files = [f for f in Path(folder).glob('*.jpg') if f.is_file()]
        for file in files:

            tempfile = str(file.absolute())
            write_log("Image file", tempfile)

            try:
                # Read e-mail Subject from .txt file
                subject = "n/a"
                txtfile = tempfile.split(".")[0] + ".txt"
                write_log("Subject file", txtfile)
                try:
                    with open(txtfile, 'r') as fb:
                        subject = fb.read()
                except Exception as err1:
                    write_log("Subject file error", err1)
                write_log("Subject text", subject)

                # Parse timestamp from the file name e.g. "Snap_20210911-184030-1.jpg"
                try:
                    split = file.stem.split("_")[1].split("-")
                    dtstr = split[0]+split[1]
                except Exception as err2:
                    dtstr = ""
                    write_log("Timestamp split error", err2)

                if dtstr:
                    timestamp = datetime.strptime(dtstr, "%Y%m%d%H%M%S")
                else:
                    timestamp = datetime.now()
                write_log("timestamp", timestamp)

                if detect_people(tempfile, file=True):
                    # Found - write to the detect table
                    data = convertToBinaryData(tempfile)
                    insertAlert(subject, timestamp, data, True)
                    write_log("Detection successfully stored to database")

            except Exception as err:
                write_log("Detection failed", err)
            finally:
                delfiles = file.stem.split(".")[0] + ".*"
                deleteFiles(delfiles)

