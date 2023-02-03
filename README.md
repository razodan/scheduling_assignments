# scheduling_assignments
by Daniel Razo.

Uses integer programming via PuLP to schedule teaching assignments optimally.

Information must be parsed in a particular way. Details to be added later.
This was originally done as project 1 for CS 6150 Advanced Algorithms at Utah Valley University during Fall 2022.
In view of academic honesty, the original project code is not included. Instead, this code has been altered to assign professors to courses. It will be further expanded to assign TA's to TA assignments.

## Things to note:
- Scheduler.py is the meat of the program. It first organizes data from cleaned_data.csv and teacher_preferences.json in order to more easily parse it. Then it uses integer programming to optimize a teaching schedule with various constraints.
- Teacher_preferences.json is a json of all instructors with their name, number of years teaching, number of credit hours requested, faculty rank, teaching preferences, days available, and times of day available. The teaching preferences are ranked as preference_1, preference_2, and preference_3. Preference_1 is such that the instructor very much wants to teach that course. Preference_2 is such that the instructor is fine with teaching that course. Preference_3 is that the instructor is able to teach that course, but perhaps would prefer not to. Then, all courses NOT listed under any preference are courses that particular professor cannot teach.
- Cleaned_data.csv is a csv of all course sections for a particular semester/trimester/etc. Column 0 is the index, column 1 is the course reference number, column 2 is the subject prefix (e.g. CS,STAT,CHEM,etc.), column 3 is the course number, column 4 is the days that section is offered, and column 5 is the time frame for that section to be taught.
- Periods.py and timetable.py interact with teacher_preferences.json by way of scheduler.py to add time period suffixes to each course. For instance, a course labeled '1400.M1' is a CS 1400 course taught from 10:00-10:50, which corresponds to an instructor giving "morning" as their availability.
- Note that cleaned_data.csv has been reduced to show only 5 courses, as an example. Also, teacher_preferences.json is only a template that must be filled by the user, given that the relevant information for each instructor is known or has been collected.

## Current limitations / to-do:
- Overlapping times are technically not accounted for.
- Does not have a user-friendly GUI. Changes have to be made in the code itself.
- Does not fully take into account instructor rank and years teaching.
- Parsing the .json and .csv files gets the job done, but it feels clunky.
- Currently assumes all courses are 3 credits.
- Currently assumes all courses hold the same prefix. e.g. Does not account for cases where a professor may teach a ENGL course as well as a PHIL course.
