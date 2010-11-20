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

## License ##

This program is [MIT][] licensed.
