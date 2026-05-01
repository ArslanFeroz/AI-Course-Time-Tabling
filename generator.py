# generator.py - Creates CSV files with different parameters for testing

import random
import csv
import os


# All slot templates - enough to cover up to 40 slots as required by assignment
ALL_SLOT_TEMPLATES = [
    ("MWF-8",   "Monday/Wednesday/Friday", "08:00", 50),
    ("MWF-9",   "Monday/Wednesday/Friday", "09:00", 50),
    ("MWF-10",  "Monday/Wednesday/Friday", "10:00", 50),
    ("MWF-11",  "Monday/Wednesday/Friday", "11:00", 50),
    ("MWF-12",  "Monday/Wednesday/Friday", "12:00", 50),
    ("MWF-1",   "Monday/Wednesday/Friday", "13:00", 50),
    ("MWF-2",   "Monday/Wednesday/Friday", "14:00", 50),
    ("MWF-3",   "Monday/Wednesday/Friday", "15:00", 50),
    ("MWF-4",   "Monday/Wednesday/Friday", "16:00", 50),
    ("MWF-5",   "Monday/Wednesday/Friday", "17:00", 50),
    ("TTh-8",   "Tuesday/Thursday", "08:00", 75),
    ("TTh-930", "Tuesday/Thursday", "09:30", 75),
    ("TTh-11",  "Tuesday/Thursday", "11:00", 75),
    ("TTh-1",   "Tuesday/Thursday", "13:00", 75),
    ("TTh-230", "Tuesday/Thursday", "14:30", 75),
    ("TTh-4",   "Tuesday/Thursday", "16:00", 75),
    # Extra MWF slots (duplicate days, different IDs) for larger instances
    ("MWF-8b",  "Monday/Wednesday/Friday", "08:00", 50),
    ("MWF-9b",  "Monday/Wednesday/Friday", "09:00", 50),
    ("MWF-10b", "Monday/Wednesday/Friday", "10:00", 50),
    ("MWF-11b", "Monday/Wednesday/Friday", "11:00", 50),
    ("MWF-12b", "Monday/Wednesday/Friday", "12:00", 50),
    ("MWF-1b",  "Monday/Wednesday/Friday", "13:00", 50),
    ("MWF-2b",  "Monday/Wednesday/Friday", "14:00", 50),
    ("MWF-3b",  "Monday/Wednesday/Friday", "15:00", 50),
    ("MWF-4b",  "Monday/Wednesday/Friday", "16:00", 50),
    ("MWF-5b",  "Monday/Wednesday/Friday", "17:00", 50),
    ("TTh-8b",  "Tuesday/Thursday", "08:00", 75),
    ("TTh-930b","Tuesday/Thursday", "09:30", 75),
    ("TTh-11b", "Tuesday/Thursday", "11:00", 75),
    ("TTh-1b",  "Tuesday/Thursday", "13:00", 75),
    ("TTh-230b","Tuesday/Thursday", "14:30", 75),
    ("TTh-4b",  "Tuesday/Thursday", "16:00", 75),
    ("MWF-8c",  "Monday/Wednesday/Friday", "08:00", 50),
    ("MWF-9c",  "Monday/Wednesday/Friday", "09:00", 50),
    ("MWF-10c", "Monday/Wednesday/Friday", "10:00", 50),
    ("MWF-11c", "Monday/Wednesday/Friday", "11:00", 50),
    ("MWF-12c", "Monday/Wednesday/Friday", "12:00", 50),
    ("MWF-1c",  "Monday/Wednesday/Friday", "13:00", 50),
    ("MWF-2c",  "Monday/Wednesday/Friday", "14:00", 50),
    ("MWF-3c",  "Monday/Wednesday/Friday", "15:00", 50),
    ("MWF-4c",  "Monday/Wednesday/Friday", "16:00", 50),
    ("MWF-5c",  "Monday/Wednesday/Friday", "17:00", 50),
    ("TTh-8c",  "Tuesday/Thursday", "08:00", 75),
    ("TTh-930c","Tuesday/Thursday", "09:30", 75),
    ("TTh-11c", "Tuesday/Thursday", "11:00", 75),
    ("TTh-1c",  "Tuesday/Thursday", "13:00", 75),
    ("TTh-230c","Tuesday/Thursday", "14:30", 75),
    ("TTh-4c",  "Tuesday/Thursday", "16:00", 75),
    ("MWF-8d",  "Monday/Wednesday/Friday", "08:00", 50),
    ("MWF-9d",  "Monday/Wednesday/Friday", "09:00", 50),
    ("MWF-10d", "Monday/Wednesday/Friday", "10:00", 50),
    ("MWF-11d", "Monday/Wednesday/Friday", "11:00", 50),
]

INSTRUCTOR_NAMES = [
    "Mr Aamir Gulzar", "Mr Arshad Islam", "Maam Marium Hida",
    "Mr Anas Bin Rashid", "Mr Hasnain Akhtar", "Mr Hasan Mujtaba",
    "Maam Bushra Kanwal",
    # Extra Pakistani names for larger instances
    "Mr Imran Butt", "Maam Sana Malik", "Mr Bilal Chaudhry",
    "Maam Nadia Hussain", "Mr Faisal Ahmed", "Maam Rabia Tariq",
    "Mr Usman Sheikh", "Maam Hira Qureshi"
]

COURSE_NAMES = [
    "Programming", "Data Structures", "Algorithms", "Databases",
    "Networks", "Operating Systems", "AI", "Machine Learning",
    "Web Development", "Cybersecurity", "Cloud Computing",
    "Software Engineering", "Compilers", "Graphics", "HCI",
    "Mobile Development", "Computer Vision", "NLP", "Robotics",
    "Distributed Systems", "Computer Architecture", "Theory of Computation",
    "Digital Logic", "Numerical Methods", "Information Security"
]

FEATURES = ["Lab", "Projector", "Whiteboard"]
DURATIONS = [50, 75]


def generate_courses(num_courses, output_dir, instructors_list):
    """Generate courses.csv - uses tightness to control how many students share courses"""
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/courses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["CourseID", "CourseName", "Instructor", "Enrollment", "Duration", "RoomFeatures"])

        for i in range(num_courses):
            course_id = f"C{i + 1:03d}"
            name = COURSE_NAMES[i % len(COURSE_NAMES)] + f" {i + 1}"
            instructor = instructors_list[i % len(instructors_list)]
            enrollment = random.randint(20, 80)
            duration = random.choice(DURATIONS)
            room_feature = random.choice(FEATURES)

            writer.writerow([course_id, name, instructor, enrollment, duration, room_feature])

    print(f"Generated {num_courses} courses")


def generate_rooms(num_rooms, output_dir):
    """Generate rooms.csv"""
    buildings = ["CS Building", "Main Building", "Lab Building", "Science Block", "Engineering Hall"]

    with open(f"{output_dir}/rooms.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["RoomID", "Building", "Capacity", "Features"])

        for i in range(num_rooms):
            room_id = f"R{i + 1:03d}"
            building = random.choice(buildings)
            capacity = random.choice([30, 40, 50, 60, 80, 100])
            # Give each room multiple features so courses can find matching rooms
            num_features = random.randint(1, 3)
            room_features = ";".join(random.sample(FEATURES, num_features))

            writer.writerow([room_id, building, capacity, room_features])

    print(f"Generated {num_rooms} rooms")


def generate_timeslots(num_slots, output_dir):
    """
    Generate timeslots.csv.
    Uses ALL_SLOT_TEMPLATES which has enough entries for up to 50 slots.
    """
    # Clamp to how many templates we have
    actual_slots = min(num_slots, len(ALL_SLOT_TEMPLATES))

    with open(f"{output_dir}/timeslots.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["SlotID", "Days", "StartTime", "Duration"])

        for i in range(actual_slots):
            slot_id, days, start, duration = ALL_SLOT_TEMPLATES[i]
            writer.writerow([slot_id, days, start, duration])

    print(f"Generated {actual_slots} time slots (requested {num_slots})")
    return actual_slots


def generate_instructor_availability(instructors_list, all_slot_ids, output_dir):
    """
    Generate instructor_availability.csv for a set of instructors and slots.
    Each instructor is available for roughly 60% of slots (enough to be solvable).
    """
    with open(f"{output_dir}/instructor_availability.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Instructor", "AvailableSlots", "PreferredSlots"])

        for instructor in instructors_list:
            # Each instructor available for at least 60% of slots
            num_available = max(3, int(len(all_slot_ids) * 0.6))
            available = random.sample(all_slot_ids, min(num_available, len(all_slot_ids)))
            available.sort()

            # Preferred slots = random subset of available (about half)
            num_preferred = max(1, len(available) // 2)
            preferred = random.sample(available, num_preferred)
            preferred.sort()

            writer.writerow([instructor, ";".join(available), ";".join(preferred)])

    print(f"Generated instructor_availability.csv for {len(instructors_list)} instructors")


def generate_students(num_students, course_ids, tightness, output_dir):
    """
    Generate students.csv.
    tightness controls how many students share courses (higher = more conflicts).
    Higher tightness means students share more courses = more student conflict constraints.
    """
    first_names = ["Ali", "Ahmed", "Sara", "Fatima", "Omar", "Zara", "Hassan",
                   "Ayesha", "Bilal", "Maryam", "Usman", "Sana", "Imran", "Hira", "Faisal"]
    last_names = ["Khan", "Malik", "Ahmed", "Ali", "Hussain", "Butt",
                  "Chaudhry", "Sheikh", "Qureshi", "Tariq", "Iqbal"]

    # tightness 0.3 = students take 2-3 courses (few conflicts)
    # tightness 0.7 = students take 5-7 courses (many conflicts)
    min_courses = max(2, int(tightness * 5))
    max_courses = max(min_courses + 1, int(tightness * 8))

    with open(f"{output_dir}/students.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["StudentID", "StudentName", "EnrolledCourses"])

        for i in range(num_students):
            student_id = f"S{i + 1:04d}"
            name = random.choice(first_names) + " " + random.choice(last_names)

            num_enrolled = random.randint(min_courses, max_courses)
            enrolled = random.sample(course_ids, min(num_enrolled, len(course_ids)))
            enrolled_str = ";".join(enrolled)

            writer.writerow([student_id, name, enrolled_str])

    print(f"Generated {num_students} students (courses per student: {min_courses}-{max_courses})")


def generate_instance(courses_count, rooms_count, slots_count,
                      density, tightness, output_dir="generated"):
    """
    Generate a complete CSP instance with given parameters.
    tightness now actually affects student course enrollment (conflict density).
    """
    print(f"\nGenerating instance with:")
    print(f"  Courses: {courses_count}")
    print(f"  Rooms: {rooms_count}")
    print(f"  Time slots: {slots_count}")
    print(f"  Constraint density: {density}")
    print(f"  Constraint tightness: {tightness}")

    os.makedirs(output_dir, exist_ok=True)

    # Pick instructors - use the 7 required ones, add more for larger instances
    num_instructors_needed = max(7, courses_count // 4)
    instructors_to_use = INSTRUCTOR_NAMES[:min(num_instructors_needed, len(INSTRUCTOR_NAMES))]

    # Generate files
    generate_courses(courses_count, output_dir, instructors_to_use)
    generate_rooms(rooms_count, output_dir)
    actual_slots = generate_timeslots(slots_count, output_dir)

    # Read back the slot IDs we just wrote
    slot_ids = []
    with open(f"{output_dir}/timeslots.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            slot_ids.append(row[0])

    # Generate instructor availability using those slot IDs
    generate_instructor_availability(instructors_to_use, slot_ids, output_dir)

    # Read back course IDs for student generation
    course_ids = []
    with open(f"{output_dir}/courses.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            course_ids.append(row[0])

    # Student count = roughly half the number of courses
    num_students = max(5, courses_count // 2)
    generate_students(num_students, course_ids, tightness, output_dir)

    print(f"Instance saved to {output_dir}/")
    print("Files: courses.csv, rooms.csv, timeslots.csv, students.csv, instructor_availability.csv")


def generate_tightness_instances(base_courses=20, output_base="instances"):
    """
    Generate instances for Experiment 3 (phase transition).
    Fixes course count at 20, varies tightness from 0.1 to 0.9.
    """
    tightness_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    for t in tightness_values:
        folder = f"{output_base}/tightness_{t}"
        generate_instance(
            courses_count=base_courses,
            rooms_count=16,
            slots_count=30,
            density=0.5,
            tightness=t,
            output_dir=folder
        )


def main():
    """Generate instances for the experiments"""

    print("=" * 50)
    print("Generating Experiment 1 instances (algorithm comparison)")
    print("=" * 50)

    # Experiment 1 instances - 5 runs each, 4 size configs
    experiments = [
        (10, 8,  20, 0.3, 0.3),
        (20, 16, 30, 0.5, 0.5),
        (30, 24, 40, 0.5, 0.5),
        (50, 40, 50, 0.7, 0.7),
    ]

    for i, (courses, rooms, slots, density, tightness) in enumerate(experiments):
        output_dir = f"instances/exp1_{i + 1}"
        generate_instance(courses, rooms, slots, density, tightness, output_dir)

    print("\n" + "=" * 50)
    print("Generating Experiment 3 instances (phase transition)")
    print("=" * 50)
    generate_tightness_instances(base_courses=20, output_base="instances")

    print("\n" + "=" * 50)
    print("Generation complete!")
    print("Check the 'instances/' folder")


if __name__ == "__main__":
    main()