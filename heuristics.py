# heuristics.py - Simple constraint checking and heuristics
# (fixed the typo from "heauristics" - sorry about that!)

def room_conflict(xi, xj):
    """Same room at same time? That's a problem."""
    return xi['room'] == xj['room'] and xi['time_slot'] == xj['time_slot']


def instructor_conflict(xi, xj, courses, course_i, course_j):
    """Same instructor can't teach two classes at once."""
    if courses[course_i]['instructor'] == courses[course_j]['instructor']:
        return xi['time_slot'] == xj['time_slot']
    return False


def student_conflict(xi, xj, course_i, course_j, conflicts):
    """Students can't be in two classes at the same time."""
    if course_j in conflicts.get(course_i, set()):
        return xi['time_slot'] == xj['time_slot']
    return False


def is_consistent(course_id, value, assignment, courses, conflicts, metrics):
    """Check if a value works with all currently assigned courses."""
    for assigned_id, assigned_value in assignment.items():
        metrics.add_constraint_check()
        if room_conflict(value, assigned_value):
            return False

        metrics.add_constraint_check()
        if instructor_conflict(value, assigned_value, courses, course_id, assigned_id):
            return False

        metrics.add_constraint_check()
        if student_conflict(value, assigned_value, course_id, assigned_id, conflicts):
            return False
    return True


def MRV_selection(assignment, courses, domains, conflicts, metrics):
    """
    Minimum Remaining Values heuristic.
    Pick the course with the fewest valid options left.
    """
    unassigned = [c for c in courses.keys() if c not in assignment]

    best_courses = []
    smallest_domain = float('inf')

    for course_id in unassigned:
        # Count how many domain values are actually consistent
        valid_count = 0
        for value in domains[course_id]:
            if is_consistent(course_id, value, assignment, courses, conflicts, metrics):
                valid_count += 1

        if valid_count < smallest_domain:
            smallest_domain = valid_count
            best_courses = [course_id]
        elif valid_count == smallest_domain:
            best_courses.append(course_id)

    # If tie, use Degree heuristic (pick course with most constraints on unassigned)
    if len(best_courses) > 1:
        assigned_set = set(assignment.keys())
        all_courses = set(courses.keys())
        unassigned_set = all_courses - assigned_set

        best_course = None
        highest_degree = -1

        for course_id in best_courses:
            neighbors = conflicts.get(course_id, set())
            degree = len([n for n in neighbors if n in unassigned_set])

            if degree > highest_degree:
                highest_degree = degree
                best_course = course_id

        return best_course

    return best_courses[0]


def LCV_selection(course_id, assignment, courses, domains, conflicts, metrics):
    """
    Least Constraining Value heuristic.
    Try values that rule out the fewest options for neighbors first.
    """
    assigned_set = set(assignment.keys())
    neighbors = conflicts.get(course_id, set())
    unassigned_neighbors = [n for n in neighbors if n not in assigned_set]

    value_impacts = []

    for value in domains[course_id]:
        if not is_consistent(course_id, value, assignment, courses, conflicts, metrics):
            continue

        # Count how many neighbor values this choice eliminates
        impact = 0
        for neighbor in unassigned_neighbors:
            for neighbor_val in domains[neighbor]:
                temp_assignment = {course_id: value}
                if not is_consistent(neighbor, neighbor_val, temp_assignment, courses, conflicts, metrics):
                    impact += 1

        value_impacts.append((value, impact))

    # Sort by impact (lowest first = least constraining)
    value_impacts.sort(key=lambda x: x[1])
    return [val for val, _ in value_impacts]