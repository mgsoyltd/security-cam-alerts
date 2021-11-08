# Surveillance Camera Alerts Server 

This is a Python3 Django web service for reviewing and administrating motion alerts of surveillance cameras from a local SQLIte3 database. 

The alert images are captured by dedicated mail and detect servers within the local network and stored into the local database. This way the surveillance alert images will be stored within your own local network.

The mail and detect services must be running prior to starting this cams service.

# Mail Server

This is a python mail server that only receives surveillance camera alert e-mails from the local network and stores the attached snapshot images to a sqlite3 database. It is also using AI people detection to create a shorter list of snapshots that may include people onto a separate table in the same database.

The **cams** web service can be used to review and administrate the alerts in the database.

Library smtpd — SMTP Server is used to build the inbound SMTP server to receive alert e-mails sent by ssecurity cameras in the local network only.

# Detect Server

This is a server that will use Artificial intelligence (AI) to detect people with computer vision in the security camera alert images and store such images into another table in the aqlite3 database.

The **cams** web service is used to review and administrate the alerts in the database.

The people recognition is built using the OpenCV Computer Vision II library **cv2** with image processing library **imutils**.