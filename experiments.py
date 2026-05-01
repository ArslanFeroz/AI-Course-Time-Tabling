# experiments.py - Runs all experiments with actual data loading

import os
import copy
import time as timer

from time_table import load_all_data
from csp import TimetableCSP
from algorithms import (
    backtracking_search,
    forward_checking_search,
    mac_search,
    min_conflicts_search
)
from heuristics import is_consistent
from Performance import Metrics


# ============================================================
# HEURISTIC VARIANTS FOR EXPERIMENT 2
# ============================================================

def first_unassigned(assignment, courses, domains, conflicts, metrics):
    """No heuristic - just pick the first unassigned course"""
    for course_id in courses:
        if course_id not in assignment:
            return course_id
    return None


def mrv_only(assignment, courses, domains, conflicts, metrics):
    """MRV only - no degree tie-breaker"""
    unassigned = [c for c in courses if c not in assignment]
    best = None
    smallest = float('inf')

    for course_id in unassigned:
        valid_count = sum(
            1 for v in domains[course_id]
            if is_consistent(course_id, v, assignment, courses, conflicts, metrics)
        )
        if valid_count < smallest:
            smallest = valid_count
            best = course_id

    return best


def mrv_degree(assignment, courses, domains, conflicts, metrics):
    """MRV + Degree - no LCV"""
    unassigned = [c for c in courses if c not in assignment]
    best_courses = []
    smallest = float('inf')

    for course_id in unassigned:
        valid_count = sum(
            1 for v in domains[course_id]
            if is_consistent(course_id, v, assignment, courses, conflicts, metrics)
        )
        if valid_count < smallest:
            smallest = valid_count
            best_courses = [course_id]
        elif valid_count == smallest:
            best_courses.append(course_id)

    if len(best_courses) > 1:
        unassigned_set = set(courses.keys()) - set(assignment.keys())
        best = None
        highest_degree = -1
        for course_id in best_courses:
            degree = len([n for n in conflicts.get(course_id, set()) if n in unassigned_set])
            if degree > highest_degree:
                highest_degree = degree
                best = course_id
        return best

    return best_courses[0] if best_courses else None


def original_order_values(course_id, assignment, courses, domains, conflicts, metrics):
    """No LCV - just return domain values in original order"""
    return [v for v in domains[course_id]
            if is_consistent(course_id, v, assignment, courses, conflicts, metrics)]


def lcv_values(course_id, assignment, courses, domains, conflicts, metrics):
    """LCV - least constraining value first"""
    assigned_set = set(assignment.keys())
    neighbors = conflicts.get(course_id, set())
    unassigned_neighbors = [n for n in neighbors if n not in assigned_set]

    value_impacts = []
    for value in domains[course_id]:
        if not is_consistent(course_id, value, assignment, courses, conflicts, metrics):
            continue
        impact = 0
        for neighbor in unassigned_neighbors:
            for nv in domains[neighbor]:
                temp = {course_id: value}
                if not is_consistent(neighbor, nv, temp, courses, conflicts, metrics):
                    impact += 1
        value_impacts.append((value, impact))

    value_impacts.sort(key=lambda x: x[1])
    return [v for v, _ in value_impacts]


def backtrack_with_heuristics(assignment, courses, domains, conflicts, metrics,
                               var_selector, val_selector):
    """Generic backtracking that accepts pluggable heuristic functions"""
    if len(assignment) == len(courses):
        return assignment

    course_id = var_selector(assignment, courses, domains, conflicts, metrics)
    if course_id is None:
        return None

    values = val_selector(course_id, assignment, courses, domains, conflicts, metrics)

    for value in values:
        assignment[course_id] = value
        metrics.add_assignment()

        result = backtrack_with_heuristics(
            assignment, courses, domains, conflicts, metrics, var_selector, val_selector
        )
        if result is not None:
            return result

        del assignment[course_id]
        metrics.add_backtrack()

    return None


# ============================================================
# EXPERIMENT 1: Algorithm Comparison
# ============================================================

def experiment_1():
    """Compare all four algorithms on instances of different sizes"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 1: Algorithm Comparison")
    print("=" * 60)

    instance_folders = [
        "instances/exp1_1",
        "instances/exp1_2",
        "instances/exp1_3",
        "instances/exp1_4",
    ]

    original_dir = os.getcwd()

    for folder in instance_folders:
        if not os.path.exists(folder):
            print(f"\n  Folder {folder} not found - run generator first")
            continue

        print(f"\n--- Instance: {folder} ---")
        os.chdir(folder)

        try:
            courses, rooms, timeslots, conflicts, instructors = load_all_data()
            csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)

            empty_domains = [c for c, d in csp.domains.items() if len(d) == 0]
            if empty_domains:
                print(f"  SKIP: {len(empty_domains)} courses have empty domains")
                os.chdir(original_dir)
                continue

            print(f"  Courses: {len(courses)}")
            print(f"\n  {'Algorithm':<20} {'Solution':<10} {'Assignments':<14} {'Backtracks':<12} {'Checks':<12} {'Time(s)':<10}")
            print("  " + "-" * 82)

            algorithms = [
                (backtracking_search,    "Backtracking",    False),
                (forward_checking_search,"Forward Checking", False),
                (mac_search,             "MAC",             False),
                (min_conflicts_search,   "Min-Conflicts",   True),
            ]

            for algo_func, algo_name, is_local in algorithms:
                fresh_domains = copy.deepcopy(csp.domains)
                metrics = Metrics()
                metrics.start_timer()

                if is_local:
                    solution = algo_func(courses, fresh_domains, conflicts, metrics)
                else:
                    solution = algo_func({}, courses, fresh_domains, conflicts, metrics)

                metrics.stop_timer()

                status = "FOUND" if solution else "FAILED"
                t = metrics.get_execution_time()
                print(f"  {algo_name:<20} {status:<10} {metrics.assignments:<14} "
                      f"{metrics.backtracks:<12} {metrics.constraint_checks:<12} {t:<10.4f}")

        except Exception as e:
            print(f"  ERROR: {e}")

        os.chdir(original_dir)


# ============================================================
# EXPERIMENT 2: Heuristic Impact
# ============================================================

def experiment_2():
    """Test four heuristic combinations using backtracking"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Heuristic Impact")
    print("=" * 60)

    # Use the medium instance (exp1_2 = 20 courses) for comparison
    folder = "instances/exp1_2"
    original_dir = os.getcwd()

    if not os.path.exists(folder):
        print(f"\n  Folder {folder} not found - run generator first")
        return

    os.chdir(folder)

    try:
        courses, rooms, timeslots, conflicts, instructors = load_all_data()
        csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)

        empty_domains = [c for c, d in csp.domains.items() if len(d) == 0]
        if empty_domains:
            print(f"  SKIP: {len(empty_domains)} courses have empty domains")
            os.chdir(original_dir)
            return

        print(f"\n  Courses: {len(courses)}")
        print(f"\n  {'Heuristic Combo':<25} {'Solution':<10} {'Assignments':<14} {'Backtracks':<12} {'Checks':<12} {'Time(s)':<10}")
        print("  " + "-" * 87)

        # 4 heuristic combinations
        combos = [
            ("No heuristics",      first_unassigned, original_order_values),
            ("MRV only",           mrv_only,         original_order_values),
            ("MRV + Degree",       mrv_degree,        original_order_values),
            ("MRV + Degree + LCV", mrv_degree,        lcv_values),
        ]

        for label, var_sel, val_sel in combos:
            fresh_domains = copy.deepcopy(csp.domains)
            metrics = Metrics()
            metrics.start_timer()

            solution = backtrack_with_heuristics(
                {}, courses, fresh_domains, conflicts, metrics, var_sel, val_sel
            )

            metrics.stop_timer()

            status = "FOUND" if solution else "FAILED"
            t = metrics.get_execution_time()
            print(f"  {label:<25} {status:<10} {metrics.assignments:<14} "
                  f"{metrics.backtracks:<12} {metrics.constraint_checks:<12} {t:<10.4f}")

    except Exception as e:
        print(f"  ERROR: {e}")

    os.chdir(original_dir)


# ============================================================
# EXPERIMENT 3: Phase Transition
# ============================================================

def experiment_3():
    """
    Phase transition analysis.
    Fix size at 20 courses, vary tightness from 0.1 to 0.9.
    Plots satisfiability rate and search cost vs tightness.
    """
    import matplotlib.pyplot as plt

    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Phase Transition Analysis")
    print("=" * 60)

    tightness_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    original_dir = os.getcwd()
    RUNS_PER_TIGHTNESS = 5

    print(f"\n  {chr(39)}Tightness{chr(39):<12} {chr(39)}Sat. Rate{chr(39):<12} {chr(39)}Avg Checks{chr(39):<14} {chr(39)}Avg Time(s){chr(39):<12}")
    print("  " + "-" * 54)

    plot_tightness = []
    plot_sat_rate = []
    plot_avg_checks = []

    for t in tightness_values:
        folder = f"instances/tightness_{t}"

        if not os.path.exists(folder):
            print(f"  {t:<12} NOT FOUND  (run generator.py first)")
            continue

        solved_count = 0
        total_checks = 0
        total_time = 0.0

        for run in range(RUNS_PER_TIGHTNESS):
            os.chdir(folder)
            try:
                courses, rooms, timeslots, conflicts, instructors = load_all_data()
                csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)
                empty_domains = [c for c, d in csp.domains.items() if len(d) == 0]
                if empty_domains:
                    os.chdir(original_dir)
                    break
                fresh_domains = copy.deepcopy(csp.domains)
                metrics = Metrics()
                metrics.start_timer()
                solution = mac_search({}, courses, fresh_domains, conflicts, metrics)
                metrics.stop_timer()
                if solution:
                    solved_count += 1
                total_checks += metrics.constraint_checks
                total_time += metrics.get_execution_time()
            except Exception as e:
                print(f"  ERROR on run {run}: {str(e)[:40]}")
            os.chdir(original_dir)

        sat_rate = solved_count / RUNS_PER_TIGHTNESS
        avg_checks = total_checks / RUNS_PER_TIGHTNESS
        avg_time = total_time / RUNS_PER_TIGHTNESS

        print(f"  {t:<12} {sat_rate:<12.2f} {avg_checks:<14.0f} {avg_time:<12.4f}")

        plot_tightness.append(t)
        plot_sat_rate.append(sat_rate)
        plot_avg_checks.append(avg_checks)

    print("\n  --- ANALYSIS ---")
    print("  Low tightness (0.1-0.3):  few student conflicts, easy to solve")
    print("  Medium tightness (0.4-0.6): more conflicts, higher search cost")
    print("  High tightness (0.7-0.9): many conflicts, may fail or take much longer")

    if not plot_tightness:
        print("\n  No data to plot - run generator.py first")
        return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    fig.suptitle("Experiment 3: Phase Transition Analysis\n(20 courses, 5 runs per tightness value)",
                 fontsize=13, fontweight="bold")

    ax1.plot(plot_tightness, plot_sat_rate, marker="o", color="steelblue",
             linewidth=2, markersize=7)
    ax1.set_xlabel("Constraint Tightness")
    ax1.set_ylabel("Satisfiability Rate")
    ax1.set_title("Satisfiability Rate vs Constraint Tightness")
    ax1.set_ylim(-0.05, 1.1)
    ax1.set_xticks(plot_tightness)
    ax1.axhline(y=0.5, color="red", linestyle="--", linewidth=1, label="50% line")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.5)

    ax2.plot(plot_tightness, plot_avg_checks, marker="s", color="darkorange",
             linewidth=2, markersize=7)
    ax2.set_xlabel("Constraint Tightness")
    ax2.set_ylabel("Average Constraint Checks")
    ax2.set_title("Search Cost vs Constraint Tightness")
    ax2.set_xticks(plot_tightness)
    ax2.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    output_path = os.path.join(original_dir, "experiment3_phase_transition.png")
    plt.savefig(output_path, dpi=150)
    plt.show()
    print(f"\n  Graph saved to: experiment3_phase_transition.png")


def experiment_4():
    """Compare MAC (systematic) with Min-Conflicts (local search)"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: Systematic vs Local Search")
    print("=" * 60)

    folder = "instances/exp1_2"
    original_dir = os.getcwd()

    if not os.path.exists(folder):
        print(f"\n  Folder {folder} not found - run generator first")
        return

    os.chdir(folder)

    try:
        courses, rooms, timeslots, conflicts, instructors = load_all_data()
        csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)

        empty_domains = [c for c, d in csp.domains.items() if len(d) == 0]
        if empty_domains:
            print(f"  SKIP: {len(empty_domains)} courses have empty domains")
            os.chdir(original_dir)
            return

        print(f"\n  Courses: {len(courses)}")

        # Run MAC
        print("\n  --- MAC (Systematic Search) ---")
        domains_mac = copy.deepcopy(csp.domains)
        metrics_mac = Metrics()
        metrics_mac.start_timer()
        solution_mac = mac_search({}, courses, domains_mac, conflicts, metrics_mac)
        metrics_mac.stop_timer()
        metrics_mac.print_report("MAC")

        # Run Min-Conflicts
        print("\n  --- Min-Conflicts (Local Search) ---")
        domains_mc = copy.deepcopy(csp.domains)
        metrics_mc = Metrics()
        metrics_mc.start_timer()
        solution_mc = min_conflicts_search(courses, domains_mc, conflicts, metrics_mc, max_steps=10000)
        metrics_mc.stop_timer()
        metrics_mc.print_report("Min-Conflicts")

        # Comparison summary
        print("\n  --- COMPARISON ---")
        print(f"  {'Metric':<25} {'MAC':>15} {'Min-Conflicts':>15}")
        print("  " + "-" * 57)
        print(f"  {'Solution found':<25} {'Yes' if solution_mac else 'No':>15} {'Yes' if solution_mc else 'No':>15}")
        print(f"  {'Assignments':<25} {metrics_mac.assignments:>15} {metrics_mc.assignments:>15}")
        print(f"  {'Backtracks':<25} {metrics_mac.backtracks:>15} {metrics_mc.backtracks:>15}")
        print(f"  {'Constraint checks':<25} {metrics_mac.constraint_checks:>15} {metrics_mc.constraint_checks:>15}")
        print(f"  {'Time (s)':<25} {metrics_mac.get_execution_time():>15.4f} {metrics_mc.get_execution_time():>15.4f}")

        print("\n  MAC: guarantees a solution if one exists; can prove unsatisfiability.")
        print("  Min-Conflicts: faster on large easy problems; cannot prove unsatisfiability.")

    except Exception as e:
        print(f"  ERROR: {e}")

    os.chdir(original_dir)


# ============================================================
# RUN ALL
# ============================================================

def run_all_experiments():
    """Run all four experiments"""
    print("\n" + "#" * 60)
    print("RUNNING ALL EXPERIMENTS")
    print("#" * 60)

    experiment_1()
    experiment_2()
    experiment_3()
    experiment_4()

    print("\n" + "#" * 60)
    print("ALL EXPERIMENTS COMPLETE")
    print("#" * 60)


if __name__ == "__main__":
    run_all_experiments()