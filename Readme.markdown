---

## About ##

This script is a grade reporting aid intended for instructors or teaching
assistants.  I wrote it to give feedback to a large class of introductory
Computer Science students.

The script will send an email to each student reporting their grade.
It a specifically crafted csv file containing:

+ Student Names
+ Student Email Addresses
+ Grades for multiple assignments
+ Comments for each individual student associated with a given assignment.

See the `testbook.csv` file as an example.

## Usage ##

Configuration is contained within the script.

If you wanted to send the students feedback on their 2nd assignment
(the 2nd one listed in their csv file), run

`./report_grades.py 2`

## Example output ##

The following is an example of what may be sent to each student
contained in the csv file.

<pre>
From: grader@example.edu
To: joe.student@example.edu
Subject: Student, Joe Cpts 111 HW9 Grade

This is an automated email report of your grade on Cpts 111 HW9.

You received 16 out of 20 points.  Additionally, the TA
had the following comments.

This is an example comment intended for the student.  It may be of 
arbitrary length.  Blablablabla.

If you have a question, or this is not you, please send an email to grader@example.edu
</pre>

## License ##

This program is [MIT][] licensed.

[MIT]:http://en.wikipedia.org/wiki/MIT_License
