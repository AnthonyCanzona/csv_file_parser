'''
Anthony Canzona
April 24, 2022
Hatchways Assesment SE 2022

Unit tests were not included as testing was based on running multiple 
instances of the script with many different passed csv test files.
'''
import sys
import csv
import json  

# Intakes args csv files
coursescsv = sys.argv[1]
studentscsv = sys.argv[2]
testscsv = sys.argv[3]
markscsv = sys.argv[4]

#Intakes args json output
outputjson = sys.argv[5]

#Checks is the course has valid grade weighting
def course_valid():
    fullcourse = {}
    with open(testscsv, 'r') as testfile:
        testreader = csv.DictReader(testfile) 

        for test in testreader:
            try: fullcourse[ str(test['course_id']) ] += float(test['weight'])
            except: fullcourse[ str(test['course_id']) ] = float(test['weight'])

        for courses in fullcourse.values():
            if (courses == 100.0): return True
            else: return False

#Calculates the students course and total average and returns a dict of the values
def student_average(stdnt_id):
    fullmarks = {}
    fullaverage = {}
    total = 0.0

    with open( markscsv, 'r') as markfile:
        markreader = csv.DictReader(markfile)
        for marks in markreader:
            if (stdnt_id == marks['student_id'] ):
                try: fullmarks[ str(marks['test_id']) ] += float(marks['mark'])
                except: fullmarks[ str(marks['test_id']) ] = float(marks['mark'])

    with open(testscsv, 'r') as testfile:
        testreader = csv.DictReader(testfile)
        for test in testreader:
            try: fullaverage[ str(test['course_id']) ] += float(fullmarks[ str(test['id']) ]) * float(test['weight']) / 100
            except: 
                try: fullaverage[ str(test['course_id']) ] = float(fullmarks[ str(test['id']) ]) * float(test['weight']) / 100
                except: pass

    for average in fullaverage.values():
        total += average / len(fullaverage.values())

    fullaverage['total'] = total
    return fullaverage

#makes and edits the dicts taken form the student.csv file to add course and averages 
with open(studentscsv, 'r') as studentfile:
    studentreader = csv.DictReader(studentfile)
    sortedstudents = sorted(studentreader, key=lambda d: d['id']) 

    for students in sortedstudents:
        classlist = []
        averages = student_average(students['id'])
        students["totalAverage"] = round(averages['total'], 2)
        averages.pop('total')

        with open(coursescsv, 'r') as coursefile:
            coursereader = csv.DictReader(coursefile) 
            for course in coursereader:
                try: 
                    course["courseAverage"] = round(averages[str(course['id'])], 2)
                    classlist.append(course)
                except: pass
            students["courses"] = classlist 

#outputs the dict as a json dump to the output file
maindict = {"students" : sortedstudents} if course_valid() else {"error": "Invalid course weights"}
x = json.dumps(maindict)
with open(outputjson, 'w') as f:
    print(x , file=f)

