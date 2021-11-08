#!python3

from os import path
from datetime import datetime
import sqlite3
import os
from detect import detect_people
from pathlib import PosixPath
from decouple import config

LOG_ACTIVE = config('LOG_ACTIVE', cast=bool)
DATABASE = config('DATABASE')

class StoreData:

    targets = ['db', 'file', 'both']

    def __init__(self, data, fnam, target, subject, timestamp, detect):
        self.data = data
        self.fnam = fnam
        self.target = target.lower()
        self.subject = subject
        self.timestamp = timestamp
        self.detect = detect
        if not self.target in self.targets:
            write_log("Invalid target")
            exit

    def process(self):
        write_log("Processing message...")
        method = getattr(self, self.target, lambda: None)
        if method:
            method()
        else:
            write_log("Invalid method!")

    def db(self):
        if self.data:
            insertAlert(self.subject, self.timestamp, self.data)
            write_log("Successfully stored to database")
            
            # People detection option
            if self.detect:
                # White image to temporary file for people detection
                storeWithDetect(self.fnam, self.subject, self.timestamp, self.data)

        else:
            write_log("No data")

    def file(self):
        if self.fnam:
            with open(self.fnam, 'wb') as fb:
                fb.write(self.data)
                write_log("Successfully stored to file: ", self.fnam)
        else:
            write_log("No file")

    def both(self):
        self.db()
        self.file()


def insertAlert(subject, timestamp, data, detected=False):
    try:
        if path.isfile(DATABASE):
            conn = sqlite3.connect(DATABASE)
            # write_log("the sqlite connection is opened")
        else:
            write_log("Invalid database path:", DATABASE)
            return
        cursor = conn.cursor()
        if detected:
            sqlite_insert_blob_query = """ INSERT INTO alerts_detect
                                    (subject, timestamp, snapshot) VALUES (?, ?, ?)"""            
        else:
            sqlite_insert_blob_query = """ INSERT INTO alerts_alert
                                    (subject, timestamp, snapshot) VALUES (?, ?, ?)"""
        # Convert data into tuple format
        data_tuple = (subject, timestamp, data)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()
        cursor.close()
        # write_log("the sqlite record inserted successfully")

    except sqlite3.Error as error:
        # if not "UNIQUE constraint failed" in error:
        write_log("Failed to insert data into sqlite table", error)

    finally:
        if conn:
            conn.close()
            # write_log("the sqlite connection is closed")


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def write_log(*args):
    if LOG_ACTIVE == True:
        timestamp = datetime.now().replace(microsecond=0)
        print(timestamp, *args)


def storeWithDetect(fnam, subject, timestamp, data):
    # Write the subject to a text file
    txtfile = fnam.split(".")[0] + ".txt"
    try:
        with open(os.open(txtfile, os.O_CREAT | os.O_WRONLY, 0o777), 'w') as fb1:
            fb1.write(subject)
    except Exception as err:
        write_log("Error creating subject file", err)

    # Write the snapshot image to a binary file
    try:
        with open(os.open(fnam, os.O_CREAT | os.O_WRONLY, 0o777), 'wb') as fb2:
            fb2.write(data)
    except Exception as err:
        write_log("Error creating snapshot file", err)        
    # Now the detect-server service should pickup files and process in background


