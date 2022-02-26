# Mail Server

This is a python mail server that only receives surveillance camera alert e-mails from the local network and stores the attached snapshot images to a sqlite3 database. It is also using AI people detection to create a shorter list of snapshots that may include people onto a separate table in the same database.

The **cams** web service can be used to review and administrate the alerts in the database.

Library smtpd — SMTP Server is used to build the inbound SMTP server to receive alert e-mails sent by security cameras in the local network only.

# Detect Server

This is a server that will use Artificial intelligence (AI) to detect people with computer vision in the security camera alert images and store such images into another table in the sqlite3 database.

The **cams** web service is used to review and administrate the alerts in the database.

The people recognition is built using the OpenCV Computer Vision II library **cv2** with image processing library **imutils**.

## Setup

Install the python3, if not done already.

After cloning this repo, do the following in the project root folder:

Create the virtual environment, activate it and install the dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Prerequisites

### SQLite3 database

An SQLite3 database called **alerts.sqlite3** must be available in a shared folder
being accessable by the **cams** Django web service and these **mail** and **detect** services.
Located e.g. in /home/**user**/db. The folder and the database file must have the owner and group set to www-data with file attributes set to 775.

To limit the records on **alerts_alert** and **alerts_detect** table, create the following triggers:

```
CREATE TRIGGER delete_alarms AFTER INSERT ON alerts_alert
    BEGIN
      DELETE FROM alerts_alert WHERE id IN (SELECT id FROM alerts_alert ORDER BY id DESC LIMIT -1 OFFSET 1000);
    END
```
```
CREATE TRIGGER delete_detect AFTER INSERT ON alerts_detect
    BEGIN
      DELETE FROM alerts_detect WHERE id IN (SELECT id FROM alerts_detect ORDER BY id DESC LIMIT -1 OFFSET 1000);
    END
```

# Environment Variables

Maintain environment variables in the .env file

```
# serve.py variables for mail server IP address, port and folder to store message attacments 
URL = '<mail_server_ip>'
PORT = '1025'
DEST_DIR = '<project_folder>/mail-server/email/msgfiles'

# store.py variable for the shared database file (shared with cams server)
DATABASE = '/home/<user>/db/alerts.sqlite3'
LOG_ACTIVE = 'True'
```

# Mail Service

The mail service is an inbound e-mail service intended to receive e-mail alerts
from the surveillance cameras within the local network. The captured images are then
stored into a table called **alerts_alert** in the SQLite3 database **alerts.sqlite3**.

These examples are made for Lubuntu 20.04.

## Run mail service manually in development 

In the project root folder 'mail-server':
```
source .venv/bin/activate
python3 serve.py
```

## Deploy as a daemon process

Create a script file /home/user/.local/bin/start_mailserver
```
echo Starting mail-server service
cd <project root folder>
source .venv/bin/activate
python3 serve.py

```

Create a service file /usr/lib/systemd/system/mymailserver.service
```
[Unit]
Description=My mailserver service for cameras

[Install]
WantedBy=default.target

[Service]
Type=simple
User=<user>
Group=adm
Restart=always
WorkingDirectory=<project root folder>
ExecStart=/bin/bash /home/<user>/.local/bin/start_mailserver
StandardOutput=null
StandardError=null
```

Start the service
```
sudo systemctl daemon-reload
sudo systemctl start mymailserver.service
sudo systemctl enable mymailserver.service
sudo systemctl list-units mymailserver*
journalctl -e -u mymailserver.service | tail

```


# Detect Service

The detect service is polling a folder for e-mail attachments i.e. images captures
by the surveillance cameras and using Artificial intelligence (AI) to detech people in the images.
Those images are then stored into a table called **alerts_detect** in the SQLite3 database
**alerts.sqlite3**.

These examples are made for Lubuntu 20.04.

## Run mail service manually in development

In the project root folder 'mail-server':
```
source .venv/bin/activate
python3 detect-server.py <project root>/email/msgfiles/
```

## Deploy as a daemon process

Create a script file /home/user/.local/bin/start_detectserver
```
echo Starting detect-server service
cd <project root folder>
source .venv/bin/activate
python3 detect-server.py <project root folder>/email/msgfiles/

```

Create a service file /usr/lib/systemd/system/mydetectserver.service
```
[Unit]
Description=My detectserver service for cameras

[Install]
WantedBy=default.target

[Service]
Type=simple
User=<user>
Group=adm
Restart=always
WorkingDirectory=<project root folder>
ExecStart=/bin/bash /home/<user>/.local/bin/start_detectserver
StandardOutput=null
StandardError=null
```

Start the service
```
sudo systemctl start mydetectserver.service
sudo systemctl enable mydetectserver.service
sudo systemctl list-units mydetectserver*
journalctl -e -u mydetectserver.service | tail
```
