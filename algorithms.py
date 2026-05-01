# algorithms.py - All four CSP algorithms we need to implement
# Backtracking, Forward Checking, MAC, and Min-Conflicts

import random
from heuristics import MRV_selection, LCV_selection, is_consistent


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def restore_domains(domains, saved_domains):
    """Restore domains after a backtrack (undoes pruning)"""
    for course_id, old_domain in saved_domains.items():
        domains[course_id] = old_domain[:]  # make a copy just to be safe


# ============================================================
# ALGORITHM 1: Basic Backtracking Search
# ============================================================

def backtracking_search(assignment, courses, domains, conflicts, metrics):
    """
    Simple backtracking - assign variables one by one,
    backtrack when we hit a dead end.

    This is the most basic approach - no domain pruning.
    """
    if len(assignment) == len(courses):
        return assignment

    # Pick next course using MRV heuristic
    course_id = MRV_selection(assignment, courses, domains, conflicts, metrics)

    # Try values in LCV order (least constraining first)
    values = LCV_selection(course_id, assignment, courses, domains, conflicts, metrics)

    for value in values:
        if is_consistent(course_id, value, assignment, courses, conflicts, metrics):
            assignment[course_id] = value
            metrics.add_assignment()

            result = backtracking_search(assignment, courses, domains, conflicts, metrics)
            if result is not None:
                return result

            # Dead end - backtrack
            del assignment[course_id]
            metrics.add_backtrack()

    return None


# ============================================================
# ALGORITHM 2: Forward Checking
# ============================================================

def forward_check(course_id, value, domains, assignment, conflicts):
    """
    Prune neighbor domains after assigning a value.
    Removes any neighbor values that conflict with our new assignment.
    """
    neighbors = [n for n in conflicts.get(course_id, []) if n not in assignment]

    for neighbor in neighbors:
        new_domain = []
        for v in domains[neighbor]:
            # Conflict if same time slot
            if v['time_slot'] != value['time_slot']:
                new_domain.append(v)

        domains[neighbor] = new_domain

        # If any neighbor has empty domain, this assignment fails
        if len(new_domain) == 0:
            return False

    return True


def forward_checking_search(assignment, courses, domains, conflicts, metrics):
    """
    Backtracking with Forward Checking.
    After each assignment, prune inconsistent values from neighbors.
    """
    if len(assignment) == len(courses):
        return assignment

    course_id = MRV_selection(assignment, courses, domains, conflicts, metrics)
    values = LCV_selection(course_id, assignment, courses, domains, conflicts, metrics)

    for value in values:
        if is_consistent(course_id, value, assignment, courses, conflicts, metrics):

            # Save current domains of neighbors so we can restore if we backtrack
            saved_domains = {}
            neighbors = [n for n in conflicts.get(course_id, []) if n not in assignment]
            for neighbor in neighbors:
                saved_domains[neighbor] = domains[neighbor][:]

            # Try to prune with forward checking
            if forward_check(course_id, value, domains, assignment, conflicts):
                assignment[course_id] = value
                metrics.add_assignment()

                result = forward_checking_search(assignment, courses, domains, conflicts, metrics)
                if result is not None:
                    return result

                # Backtrack
                del assignment[course_id]
                metrics.add_backtrack()

            # Restore domains
            restore_domains(domains, saved_domains)

    return None


# ============================================================
# ALGORITHM 3: MAC (Maintaining Arc Consistency)
# ============================================================

def revise(xi, xj, domains):
    """
    Revise the domain of xi by removing values that have no support in xj.
    Returns True if the domain changed.
    """
    revised = False

    for val_i in domains[xi][:]:  # iterate over a copy
        # Check if there's ANY value in xj that doesn't conflict
        has_support = False
        for val_j in domains[xj]:
            if val_i['time_slot'] != val_j['time_slot']:
                has_support = True
                break

        if not has_support:
            domains[xi].remove(val_i)
            revised = True

    return revised


def ac3(domains, conflicts, assignment):
    """
    AC-3 algorithm - makes the problem arc consistent.
    Returns False if any domain becomes empty.
    """
    # Create queue of all arcs (Xi, Xj) where Xi and Xj share a constraint
    queue = []
    for xi in domains:
        for xj in conflicts.get(xi, []):
            if xj in domains:  # make sure it's still a variable
                queue.append((xi, xj))

    while queue:
        xi, xj = queue.pop(0)

        if revise(xi, xj, domains):
            if len(domains[xi]) == 0:
                return False  # domain wipeout

            # Add all arcs (Xk, Xi) back to queue
            for xk in conflicts.get(xi, []):
                if xk != xj and xk in domains:
                    queue.append((xk, xi))

    return True


def mac_search(assignment, courses, domains, conflicts, metrics):
    """
    Maintaining Arc Consistency - like forward checking but stronger.
    After each assignment, run AC-3 to enforce consistency everywhere.
    """
    if len(assignment) == len(courses):
        return assignment

    course_id = MRV_selection(assignment, courses, domains, conflicts, metrics)
    values = LCV_selection(course_id, assignment, courses, domains, conflicts, metrics)

    for value in values:
        if is_consistent(course_id, value, assignment, courses, conflicts, metrics):

            # Save ALL domains (we need to restore everything if we backtrack)
            saved_domains = {c: domains[c][:] for c in domains}

            # Make the assignment
            assignment[course_id] = value
            metrics.add_assignment()

            # Prune this value from other domains (like forward check)
            forward_check(course_id, value, domains, assignment, conflicts)

            # Run AC-3 to make everything consistent
            if ac3(domains, conflicts, assignment):
                result = mac_search(assignment, courses, domains, conflicts, metrics)
                if result is not None:
                    return result

            # Backtrack
            del assignment[course_id]
            metrics.add_backtrack()
            restore_domains(domains, saved_domains)

    return None


# ============================================================
# ALGORITHM 4: Min-Conflicts Local Search
# ============================================================

def count_conflicts(course_id, value, assignment, conflicts):
    """
    Count how many conflicts this assignment would have.
    """
    conflict_count = 0

    for neighbor in conflicts.get(course_id, []):
        if neighbor in assignment:
            neighbor_val = assignment[neighbor]
            # Conflict if same time slot
            if value['time_slot'] == neighbor_val['time_slot']:
                conflict_count += 1

    return conflict_count


def get_conflicted_courses(assignment, conflicts):
    """Find all courses that are currently in conflict"""
    conflicted = []

    for course_id in assignment:
        if count_conflicts(course_id, assignment[course_id], assignment, conflicts) > 0:
            conflicted.append(course_id)

    return conflicted


def get_min_conflict_value(course_id, assignment, domains, conflicts):
    """
    Find the value that causes the fewest conflicts.
    Breaks ties randomly.
    """
    best_value = None
    best_count = float('inf')

    # Shuffle so ties are broken randomly
    shuffled_domain = domains[course_id][:]
    random.shuffle(shuffled_domain)

    for value in shuffled_domain:
        conflicts_count = count_conflicts(course_id, value, assignment, conflicts)

        if conflicts_count < best_count:
            best_count = conflicts_count
            best_value = value

            # Can't do better than 0
            if best_count == 0:
                break

    return best_value


def min_conflicts_search(courses, domains, conflicts, metrics, max_steps=10000):
    """
    Min-Conflicts local search.
    Start with a random complete assignment, then iteratively fix conflicts.
    """
    # Create random initial assignment
    assignment = {}
    for course_id in courses:
        assignment[course_id] = random.choice(domains[course_id])
        metrics.add_assignment()

    for step in range(max_steps):
        # Find all conflicted courses
        conflicted = get_conflicted_courses(assignment, conflicts)

        # No conflicts? We're done!
        if not conflicted:
            return assignment

        # Pick a random conflicted course to fix
        course_id = random.choice(conflicted)

        # Reassign it to the value with fewest conflicts
        best_value = get_min_conflict_value(course_id, assignment, domains, conflicts)
        assignment[course_id] = best_value
        metrics.add_assignment()

    # Ran out of steps
    return None