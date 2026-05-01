# time_table.py - Loads all the CSV data files

import pandas as pd
import os


def load_all_data():
    """
    Loads and processes all the CSV files.
    Returns a tuple of (courses, rooms, timeslots, conflicts, instructors)
    """

    # Load CSV files inside the function so os.chdir() in experiments works correctly
    courses_df = pd.read_csv("courses.csv")
    rooms_df = pd.read_csv("rooms.csv")
    timeslots_df = pd.read_csv("timeslots.csv")
    students_df = pd.read_csv("students.csv")

    # instructor_availability.csv is optional - generated instances may not have it
    if os.path.exists("instructor_availability.csv"):
        instructor_avail_df = pd.read_csv("instructor_availability.csv")
    else:
        instructor_avail_df = pd.DataFrame(columns=["Instructor", "AvailableSlots", "PreferredSlots"])

    # ----- Load courses -----
    courses = {}
    for _, row in courses_df.iterrows():
        courses[row['CourseID']] = {
            'name': row['CourseName'],
            'instructor': row['Instructor'],
            'enrollment': int(row['Enrollment']),
            'duration': int(row['Duration']),
            'features': set(row['RoomFeatures'].split(';'))
        }

    # ----- Load rooms -----
    rooms = {}
    for _, row in rooms_df.iterrows():
        rooms[row['RoomID']] = {
            'building': row['Building'],
            'capacity': int(row['Capacity']),
            'features': set(row['Features'].split(';'))
        }

    # ----- Load time slots -----
    timeslots = {}
    for _, row in timeslots_df.iterrows():
        timeslots[row['SlotID']] = {
            'days': row['Days'],
            'start_time': row['StartTime'],
            'duration': int(row['Duration'])
        }

    # ----- Build student conflict graph -----
    # Two courses conflict if they share at least one student
    student_courses = {}
    for _, row in students_df.iterrows():
        student_courses[row['StudentID']] = row['EnrolledCourses'].split(';')

    course_conflicts = {}
    for student, enrolled in student_courses.items():
        for i in range(len(enrolled)):
            for j in range(i + 1, len(enrolled)):
                c1, c2 = enrolled[i], enrolled[j]

                if c1 not in course_conflicts:
                    course_conflicts[c1] = set()
                if c2 not in course_conflicts:
                    course_conflicts[c2] = set()

                course_conflicts[c1].add(c2)
                course_conflicts[c2].add(c1)

    # ----- Load instructor availability -----
    instructors = {}
    for _, row in instructor_avail_df.iterrows():
        instructors[row['Instructor']] = {
            'available': row['AvailableSlots'].split(';') if pd.notna(row['AvailableSlots']) else [],
            'preferred': row['PreferredSlots'].split(';') if pd.notna(row['PreferredSlots']) else []
        }

    return courses, rooms, timeslots, course_conflicts, instructors