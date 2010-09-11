#!/usr/bin/python
#
# Running on python 2.6.5
#
# This script is used to report grades on specific assignments along with
# individualized feedback comments to a large class via email.
#
# This script uses msmtp to send mail since I'm scared of the python.
#
# This is a simple script which reads in a specifically formatted csv file,
# in which the first two rows are labels and headers, 
#
#       Name, Email, Assignment     , Assign. 1                , Comments on Assignment 1, Assign. 2	         , ...
#	    ,      , Points Possible, <max points of Assign. 1>,                         , <max points Assign. 2>, ...
#
#
#
# starting with row three, the columns begin containing data.
#
#	Usage:
#		./report_grades.py NUMBER, where NUMBER is the assignment number
#			                   of the grades that you want to send.
#


import sys
import csv
import os

debugging = 0 # set to 0 if not debugging
classname = "Class Name"
grader_email = "me@example.edu"

def usage():
	print("Usage: ./report_grades.py NUMBER, where NUMBER is the assignment number")
	print("                                  of the grades that you want to send.\n\n")

def mail_send(student_email, student_name, classname, homeworkname, body):
	p = os.popen('msmtp -t','w')
	message = "To: " + student_email + "\nSubject: " + student_name + " " + classname + " " + homeworkname + " Grade\n\n" + body
	p.write(message)
	p.close

# Begin the main function
if len(sys.argv) != 2: # the program name and the assignment number
	usage()
	sys.exit(2)

points_col = 2 * (int(sys.argv[1]) - 1) + 3 # get the row that the points are in
comment_col = points_col + 1		    # comments are in the next row

#data = csv.reader(open('Gradebook.csv', 'rb'), delimiter=',', quotechar='"')
data = csv.reader(open('testbook.csv', 'rb'), delimiter=',', quotechar='"')

for row in data:
	# our header in the first two rows contains information we need, strip it out
	if data.line_num == 1: # first row
		homeworkname = row[points_col]
	elif data.line_num == 2: # second row
		maxpoints = row[points_col]

		if debugging == 1:
			print "What values are we getting?"
			print "Classname: " + classname
			print "Homeworkname: " + homeworkname

	else: # we're in the data section
		student_name = row[0]
		student_email = row[1]
		grade = row[points_col]
		comment = row[comment_col]

		# form the email body
		body = "This is an automated email report of your grade on " + classname + " " +  homeworkname + ".\n\nYou received " + grade + " out of " + maxpoints + " points.  Additionally, the TA\nhad the following comments.\n\n" + comment
		body = body + "\n\nIf you have a question, or this is not you, please send an email to " + grader_email + ".\n"

		if debugging == 1:
			if 2 < data.line_num < 8: # only return the first few
				
				# give an example of the email body to be sent
				print(body)

		else: # send the message
			mail_send(student_email, student_name, classname, homeworkname, body)
