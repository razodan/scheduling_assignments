'''
Format:
Some_timetable = [
    ('LABEL1','00:00-00:00'),
    ('LABEL2','00:00-00:00'),
    ...,
    ('LABEL-N','00:00-00:00')
]

Each label maps to a prefix in periods.py, which maps to a times[timeOfDay] label in teacher_preferences.json.
Thus corresponds to a time prefix for any given section of a course.
For example, M1.1400 means that a particular section of CS 1400 is taught at 10:00-10:50.
    Thus, an instructor with "morning" in times[timeOfDay] has time to teach that course.
'''

M_TIMETABLE = [
    ('M1','10:00-10:50'),
    ('M2','11:00-11:50'),
    ('M3','12:00-12:50'),
    ('M4','13:00-14:15'),
    ('M5','14:00-14:50'),
    ('M6','14:30-15:45'),
    ('M7','16:00-17:15'),
    ('M8','17:30-18:45'),
    ('M9','19:00-20:15')
]

T_TIMETABLE = [
    ('T1','08:30-09:45'),
    ('T2','10:00-11:15'),
    ('T3','11:30-12:45'),
    ('T4','13:00-14:15'),
    ('T5','14:30-15:45'),
    ('T6','16:00-17:15'),
    ('T7','17:30-18:45')
]