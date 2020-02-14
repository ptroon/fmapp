# Imports
from project import app, db, is_admin, mail
from flask_mail import Message
import os

# This python script will carry out the jobs stored in the database marked as
# runnable, not started and not completed.
#
# Jobs include sending emails and housekeeping tasks
#
# Set the crontab to run the calling script every 5 minutes as:
# */5 * * * * <user> <folder_for_app>/fmapp/jobs.sh
#
# Run application
if __name__ == '__main__':

    #jobs = db.session.query(Job).order_by(Job.id.asc())

    print("Testing.. " + app.config["MAIL_SERVER"])
