#!/usr/bin/python
#
# Running on python 2.6.5
#
# This script is used to report grades on specific assignments along with
# individualized feedback comments to a large class via email.
#
# This is a simple script which reads in a specifically formatted csv file,
# in which the first two rows are labels and headers,
#
#       Name, Email, Assignment     , Assign. 1        , Comments on Assignment 1, Assign. 2	     , ...
#	    ,      , Points Possible, <max points of Assign. 1>,             , <max points Assign. 2>, ...
#
#
#
# starting with row three, the columns begin containing data.
#
#	Usage:
#		./hw_harbinger.py NUMBER, where NUMBER is the assignment number
#			           of the grades that you want to send.
#

import sys
import csv
import smtplib

#================================== Configuration Options ==========================================#

debugging = 1 # Set to 0 if not debugging (when debugging, no mails are sent).
	      # This option is mostly for making sure that the script parses
	      # the gradebook file correctly.

classname = "Class Name"
grader_email = "me@example.edu"

gradebook = "testbook.csv" # include the full path, if not in this directory

messagefile = "common_message.txt"  # If you want to include a common message
                  # to all students at the beginning of every
                  # email, specify the file name here.
                  # Otherwise, leave as an empty string

FEEDBACK = 1 # enable feedback every 10 students

# smtp server settings
smtpserver = "mail.example.edu:25"
USE_SSL = 0 # switch to 1 if you want to connect with SSL

AUTHREQUIRED = 0 # if you need to use smtp auth, set to 1
smtpuser = "" # for SMTP AUTH, set SMTP username here
smtppass = "" # for SMTP AUTH, set SMTP password here

#============================= End configuration, Begin the script ==================================#

def usage():
    print("Usage: ./hw_harbinger.py NUMBER, where NUMBER is the assignment number")
    print("                                  of the grades that you want to send.\n\n")

def mail_send(grader_email, student_email, message):

    if USE_SSL:
        session = smtplib.SMTP_SSL(smtpserver)
    else:
        session = smtplib.SMTP(smtpserver)
    if AUTHREQUIRED:
        session.login(smtpuser, smtppass)

    #check to see if any errors occured
    smtpresult = session.sendmail(grader_email,student_email,message)

    if smtpresult:
        errstr = ""
        for recip in smtpresult.keys():
            errstr = ("Could not deliver mail to %s" +
                        "Server said %s" + "%s" + "%s"
                        % (recip, smtpresult[recip][0], smtpresult[recip][1], errstr))
            raise smtplib.SMTPException, errstr
    else: # if there were not errors, close the smtp session
        session.quit()

def prepend_message():

    if messagefile != "":
        try:
            handle = open(messagefile, "r")
        except:
            print("Couldn't open the message file `"+messagefile +"`. Exiting.")
            sys.exit(3)

        message = handle.read()
        handle.close()
        return message


def main(args):
    points_col = 2 * (int(args[1]) - 1) + 3 # get the column that the points are in
    comment_col = points_col + 1	    # comments are in the next column

    data = csv.reader(open(gradebook, 'rb'), delimiter=',', quotechar='"')

    prepend = prepend_message()

    for row in data:
        # our header in the first two rows contains information we need, strip it out
        if data.line_num == 1: # first row
            homeworkname = row[points_col].strip()
        elif data.line_num == 2: # second row
            maxpoints = row[points_col].strip()

            if debugging == 1:
                print("What values are we getting?")
                print("Classname: " + classname)
                print("Homeworkname: " + homeworkname)

        else: # we're in the data section
            if FEEDBACK and (not ((data.line_num - 2) % 10)):
                print("Reporting to student " + str(data.line_num-2) + " ...")

            student_name = row[0].strip()
            student_email = row[1].strip()
            grade = row[points_col].strip()
            comment = row[comment_col].strip()

            # form the email body
            body = ""
            if prepend:
                body += prepend + "\n"

            body += ("This is an automated email report of your grade for " + classname +
                " " +  homeworkname + ".\n\n")
            body += ("You received " + grade + " out of " + maxpoints + " points.")

            if len(comment) > 0:
                body += ("\n\nAddtionally, the TA had the following comments:\n\n"
                    + comment)

            body += ("\n\nIf you have a question, or my email script made a mistake,\n"
                + "please send me an email at " + grader_email + ".\n")

            if debugging == 1:
                if 2 < data.line_num < 8: # only return the first few

                    # give an example of the email body to be sent
                    print(body)

            else: # send the message
                message = ("To: " + student_email + "\r\nSubject: " +
                    student_name + " " + classname + " " +
                    homeworkname + " Grade\r\n\r\n" + body)

                mail_send(grader_email, student_email.split(), message)

    if FEEDBACK:
        print("\nFinished reporting to a total of "+str(data.line_num-2)
                +" students.\n")

if __name__ == '__main__':
    if len(sys.argv) != 2: # the program name and the assignment number
        usage()
        sys.exit(2)
    else:
        main(sys.argv)

