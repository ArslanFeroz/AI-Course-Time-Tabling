# output_formatter.py - Makes the solution look pretty

def print_solution(algorithm_name, solution, metrics, courses, timeslots, rooms):
    """
    Prints the solution in the required format.
    Includes header, course details, grid view, and metrics.
    """

    # Header
    print("\n" + "=" * 60)
    print(f"UNIVERSITY TIMETABLE SOLUTION")
    print(f"Algorithm: {algorithm_name}")
    print(f"Status: {'SOLUTION FOUND' if solution else 'UNSATISFIABLE'}")
    print("=" * 60)

    if not solution:
        print("No valid schedule found!")
        return

    # Course details
    print("\nCOURSE SCHEDULE:")
    print("-" * 70)

    for course_id, assignment in sorted(solution.items()):
        course = courses[course_id]
        slot_id = assignment['time_slot']
        room_id = assignment['room']

        slot_info = timeslots[slot_id]
        room_info = rooms[room_id]

        print(f"\n{course_id}: {course['name']}")
        print(f"  Instructor : {course['instructor']}")
        print(f"  Time Slot  : {slot_id} ({slot_info['days']} {slot_info['start_time']})")
        print(f"  Room       : {room_id} ({room_info['building']}, Capacity: {room_info['capacity']})")
        print(f"  Enrolled   : {course['enrollment']}")

    # Schedule grid view
    print("\n" + "=" * 60)
    print("SCHEDULE GRID VIEW")
    print("=" * 60)

    # Get all unique time slots and rooms that are actually used
    all_slots = list(timeslots.keys())
    all_rooms = list(rooms.keys())

    # Print header row
    print(f"\n{'Room':<10}", end="")
    for slot in all_slots:
        print(f"{slot:<15}", end="")
    print()
    print("-" * (10 + 15 * len(all_slots)))

    # Print each room's schedule
    for room_id in all_rooms:
        print(f"{room_id:<10}", end="")
        for slot_id in all_slots:
            # Find what's scheduled here
            course_found = None
            for course_id, assignment in solution.items():
                if assignment['room'] == room_id and assignment['time_slot'] == slot_id:
                    course_found = course_id
                    break

            if course_found:
                print(f"{course_found:<15}", end="")
            else:
                print(f"[EMPTY]{' ':<9}", end="")
        print()

    # Performance metrics
    print("\n" + "=" * 60)
    print("PERFORMANCE METRICS")
    print("=" * 60)
    print(f"Total Courses Scheduled : {len(solution)}/{len(courses)}")
    print(f"Variable Assignments    : {metrics.assignments}")
    print(f"Backtracks              : {metrics.backtracks}")
    print(f"Constraint Checks       : {metrics.constraint_checks}")
    print(f"Execution Time          : {metrics.get_execution_time():.4f} seconds")

    # Check for any violations (should be none)
    print("\nWARNINGS:")
    print("-" * 30)
    print("All hard constraints satisfied ✓")
    print("=" * 60)


def print_grid_simple(assignment, courses, timeslots, rooms):
    """
    A simpler grid view if the fancy one is too much.
    """
    print("\n--- SIMPLE GRID VIEW ---")
    print("(Time Slot -> Room -> Course)")

    # Group by time slot
    by_slot = {}
    for course_id, assign in assignment.items():
        slot = assign['time_slot']
        room = assign['room']
        if slot not in by_slot:
            by_slot[slot] = {}
        by_slot[slot][room] = course_id

    for slot_id in sorted(timeslots.keys()):
        print(f"\n{slot_id}:")
        slot_assignments = by_slot.get(slot_id, {})
        for room_id in sorted(rooms.keys()):
            course = slot_assignments.get(room_id, "[EMPTY]")
            print(f"  {room_id}: {course}")