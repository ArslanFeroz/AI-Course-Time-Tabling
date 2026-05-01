# debug_domains.py - Check why domains are empty

from time_table import load_all_data
from csp import TimetableCSP

print("=" * 60)
print("DEBUGGING EMPTY DOMAINS")
print("=" * 60)

# Load data
courses, rooms, timeslots, conflicts, instructors = load_all_data()

print(f"\nLoaded {len(courses)} courses")
print(f"Loaded {len(rooms)} rooms")
print(f"Loaded {len(timeslots)} time slots")

# Create CSP
csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)

print("\n" + "=" * 60)
print("DOMAIN SIZES PER COURSE")
print("=" * 60)

empty_courses = []

for course_id, domain in csp.domains.items():
    print(f"\n{course_id}: {len(domain)} valid (time,room) pairs")

    if len(domain) == 0:
        empty_courses.append(course_id)

        # Show why this course has no options
        course = courses[course_id]
        print(f"  → This course has NO valid assignments!")
        print(f"     Course duration: {course['duration']} min")
        print(f"     Required features: {course['features']}")
        print(f"     Enrollment: {course['enrollment']}")
        print(f"     Instructor: {course['instructor']}")

        # Check time slots
        valid_times = []
        for slot_id, slot in timeslots.items():
            if slot['duration'] == course['duration']:
                valid_times.append(slot_id)
        print(f"     Time slots with matching duration: {valid_times}")

        # Check instructor availability
        if course['instructor'] in instructors:
            avail = instructors[course['instructor']]['available']
            print(f"     Instructor available slots: {avail}")

        # Check rooms
        valid_rooms = []
        for room_id, room in rooms.items():
            if course['features'].issubset(room['features']):
                if room['capacity'] >= course['enrollment']:
                    valid_rooms.append(room_id)
        print(f"     Rooms with required features + capacity: {valid_rooms}")

print("\n" + "=" * 60)
if empty_courses:
    print(f"❌ {len(empty_courses)} courses have empty domains: {empty_courses}")
    print("\nPossible fixes:")
    print("1. Add more time slots to timeslots.csv")
    print("2. Add more rooms to rooms.csv")
    print("3. Relax instructor availability constraints")
    print("4. Check if course duration matches any time slot")
else:
    print("✅ All courses have at least one valid assignment!")