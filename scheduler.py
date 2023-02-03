'''
By Daniel Razo. First started in September 2022.

This program has two parts.

    Part One: Collects course section data for a given semester in the form of a csv and
    organizes it into a list. Then, collects instructor information (name, number of
    years teaching experience, faculty rank, course preferences, availability) from a
    .json file and puts that into a list of dictionaries. Lastly, collects all possible
    combinations of instructor/course-sections, and organizes those combinations into a
    list of strings in the format "InstructorName->CourseSection" (e.g. "Alex Rodriguez->1410.M6").

    Part Two: Uses the PuLP package to perform integer programming and optimize a teaching
    schedule for the semester, provided each professor's teaching preferences and daily
    availability, as well as a set of constraints, which are as follows:
        1. Each instructor shall teach no less than 3 sections.
        2. Each instructor shall teach no more than 4 sections.
        3. Each instructor shall teach no more than 2 sections of a given course.
        4. Each section shall be assigned exactly 1 instructor.
    Sections that are not filled by faculty are to be filled by adjunct instructors.
    All courses are presumed to be 3 credit hours in this case.
    The constraints may be altered as desired.
'''
import json
import csv
import numpy as np
from pulp import LpConstraint,LpAffineExpression,LpVariable,LpProblem,LpMaximize
from periods import PERIODS
from timetable import M_TIMETABLE,T_TIMETABLE

### PART ONE -- Data Preprocessing -- consider moving this to another file.
# iterate through cleaned_data.csv
# iterate through teacher_preferences.json
# match sections with timetable.py and periods.py
# concatenate the data to make it usable
Courses_I = []
Instructors_J = []
Sections_K = []
avail_sections = [] # number of available sections, according to index
weights = []
num_requested = []

### Prepare course data
with open("cleaned_data.csv","r") as csvfile:
    next(csvfile)
    prev = ""
    index = -1
    for row in csv.reader(csvfile):
        c = row[3]
        if c == prev:
            Courses_I[index]["Sections"]+=1
            Courses_I[index]["Section Times"].append((row[4],row[5]))
        else:
            Courses_I.append({"Course":c,"Sections":1,"Section Times":[(row[4],row[5])]})
            prev = c
            index+=1

Courses_I.reverse()

### Prepares all sections in a list
for line in Courses_I:
    avail_sections.append(line["Sections"])
    for sec in line["Section Times"]:
        if sec[0][0] in 'MWF':
            for x in M_TIMETABLE:
                if sec[1] == x[1]:
                    newentry = line["Course"] + '.' + x[0]
                    Sections_K.append(newentry)
        if sec[0][0] in 'TR':
            for x in T_TIMETABLE:
                if sec[1] == x[1]:
                    newentry = line["Course"] + '.' + x[0]
                    Sections_K.append(newentry)

prof = []
asso = []
assi = []
lect = []
org_by_years = []

file = open("teacher_preferences.json")
Instructors_J = json.load(file)
for i in range(len(Instructors_J)):
    j = i
    Instructors_J[i]["responsibilities"] = []
    while j > 0 and Instructors_J[j]['numYearsTeaching'] < Instructors_J[j-1]['numYearsTeaching']:
        temp = Instructors_J[j-1]
        Instructors_J[j-1] = Instructors_J[j]
        Instructors_J[j] = temp
        j = j-1
    i=i+1
Instructors_J.reverse()

dyct = {}
for ins in Instructors_J:
    lyst = []
    dyct[ins['name']] = lyst
    num_sections_requested = ins['numHoursRequested'] / 3
    num_requested.append(num_sections_requested)
    for sec in Sections_K:
        ### Check availability and preferences
        # print(sec)
        val = 0

        cannot_teach = False
        time_pref = ins['times']
        if len(time_pref['days']) != 0:
            # if there is a time preference, set cannot_teach to True
            # then reset to False if time slots align
            cannot_teach = True
            for time in PERIODS:
                if sec[-2:] in PERIODS[time] and time in time_pref['timeOfDay'] and sec[-2:-1] in time_pref['days']:
                    cannot_teach = False
        # if instructor's time slots do not align, do not check preferences
        if cannot_teach is False:  
            if sec[:4] in ins['preference_1']:
                val = 3
            elif sec[:4] in ins['preference_2']:
                val = 2
            elif sec[:4] in ins['preference_3']:
                val = 1
        weights.append(val)
        lyst.append((sec,val))

total_sections = len(Sections_K)
total_courses = len(Courses_I)
total_instructors = len(Instructors_J)

assignments = []

for j in Instructors_J:
    for k in Sections_K:
        entry = j['name'] + "->" + k
        assignments.append(entry)
        
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

### PART TWO - Integer Programming
# Maximization variable.
maxim = LpProblem("Scheduling",LpMaximize)

# List of LpVariable objects, each of which is an instructor-section matchup.
# 0 if instructor is not teaching the section.
# 1 if instructor is teaching the section.
each_assignment = [LpVariable(assignments[i],lowBound=0,upBound=1,cat='Integer') for i in range(len(assignments))]

# Objective function.
# each_assignment[i] is either 0 or 1, multiplied by the preference weight for that section.
obj = LpAffineExpression((each_assignment[i],weights[i]) for i in range(len(assignments)))

# initialize empty constraints
keyint = 1
lowbound = 0
CONS_1 = LpConstraint()
CONS_2 = LpConstraint()
CONS_3 = LpConstraint()
CONS_4 = LpConstraint()
CONS_5 = LpConstraint()

# Feels a bit clunky with all these nested loops, but it works just fine.
for key in dyct:
    rang = range(lowbound,total_sections*keyint)
    # No instructor shall teach more than 4 sections
    CONS_1 = (sum([each_assignment[i] for i in range(lowbound,total_sections*keyint)]) <= num_requested[keyint-1])
    # No instructor shall teach fewer than 3 sections
    CONS_2 = (sum([each_assignment[i] for i in range(lowbound,total_sections*keyint)]) >= 3)
    maxim += CONS_1
    maxim += CONS_2

    # Loop for constraint 3
    for c in Courses_I:
        number = c['Course']
        indices = []

        # iterate through the corresponding instructor's sections
        for z in range(lowbound,total_sections*keyint):
            if str(each_assignment[z])[-7:-3] == number:
                indices.append(z) # append all sections which match the given course number
        # No instructor shall teach more than 2 sections of a given course
        CONS_3 = (sum([each_assignment[i] for i in indices]) <= 2)
        maxim+= CONS_3
    lowbound = total_sections*keyint
    keyint += 1

    unflattened_times = [x for x in PERIODS.values()]
    the_times = []
    [the_times.extend(list) for list in unflattened_times]
    for t in the_times:
        indices = []
        for n in rang:
            if assignments[n][-2:] == t:
                indices.append(n)

        # No instructor shall teach more than 1 section at the same time
        CONS_5 = (sum([each_assignment[i] for i in indices]) <= 1)
        maxim += CONS_5


i = 0
# Loop for constraint 4
for section in Sections_K:
    nxt = i
    a = 0
    indices = []
    # For a given section, get LpVariableVal for each instructor
    while nxt % total_sections == i and a < len(Instructors_J):
        indices.append(nxt)
        nxt+=total_sections
        a+=1
    # No section shall be taught by more than one instructor.
    CONS_4 = (sum([each_assignment[nxt] for nxt in indices]) <= 1)
    maxim += CONS_4
    i+=1

maxim += obj
maxim.solve()

# Display each LpVariable which has a value of 1
# i.e. display all instructor-section pairs that hold true.
x = [each_assignment[i].varValue for i in range(len(assignments))]
varvals = [assignments[i] for i in range(len(assignments)) if x[i] != 0.0]
for x in varvals:
    print(x)
