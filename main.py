# python main.py --algorithm mac
# python main.py --algorithm backtrack
# python main.py --algorithm forward
# python main.py --algorithm minconflicts
#
# runing all experiments
# python main.py --experiment 1
#
#
# test_generation
# python main.py --generate --courses 20 --rooms 16 --output-dir instances/my_test


import argparse
import sys
import os

from time_table import load_all_data
from csp import TimetableCSP
from algorithms import (
    backtracking_search,
    forward_checking_search,
    mac_search,
    min_conflicts_search
)
from Performance import Metrics
from output_formatter import print_solution
from experiments import run_all_experiments
from generator import generate_instance


def solve_with_algorithm(algorithm_name, courses, domains, conflicts):
    """Run a specific algorithm and return the solution and metrics"""
    metrics = Metrics()
    assignment = {}

    print(f"\nRunning {algorithm_name}...")

    metrics.start_timer()

    if algorithm_name == "backtrack":
        solution = backtracking_search(assignment, courses, domains, conflicts, metrics)
    elif algorithm_name == "forward":
        solution = forward_checking_search(assignment, courses, domains, conflicts, metrics)
    elif algorithm_name == "mac":
        solution = mac_search(assignment, courses, domains, conflicts, metrics)
    elif algorithm_name == "minconflicts":
        solution = min_conflicts_search(courses, domains, conflicts, metrics)
    else:
        print(f"Unknown algorithm: {algorithm_name}")
        return None, None

    metrics.stop_timer()

    return solution, metrics


def main():
    """Main entry point - parses command line arguments"""

    parser = argparse.ArgumentParser(description="CSP University Timetabling")
    parser.add_argument("--input-dir", default=".", help="Directory containing CSV files")
    parser.add_argument("--algorithm", choices=["backtrack", "forward", "mac", "minconflicts"],
                        default="mac", help="Which algorithm to run")
    parser.add_argument("--generate", action="store_true", help="Generate test instances")
    parser.add_argument("--courses", type=int, default=20, help="Number of courses to generate")
    parser.add_argument("--rooms", type=int, default=16, help="Number of rooms to generate")
    parser.add_argument("--density", type=float, default=0.5, help="Constraint density")
    parser.add_argument("--output-dir", default="instances/test", help="Output directory for generation")
    parser.add_argument("--experiment", type=int, choices=[1, 2, 3, 4], help="Run specific experiment")

    args = parser.parse_args()

    # Handle instance generation
    if args.generate:
        generate_instance(args.courses, args.rooms, 20, args.density, 0.5, args.output_dir)
        return

    # Handle experiments - run only the selected one
    if args.experiment:
        from experiments import experiment_1, experiment_2, experiment_3, experiment_4
        exp_map = {1: experiment_1, 2: experiment_2, 3: experiment_3, 4: experiment_4}
        exp_map[args.experiment]()
        return

    # Normal solve mode
    print("\n" + "=" * 60)
    print("CSP UNIVERSITY TIMETABLING SOLVER")
    print("=" * 60)

    # Load data
    print(f"\nLoading data from {args.input_dir}...")

    # Change to input directory if needed
    if args.input_dir != ".":
        os.chdir(args.input_dir)

    try:
        courses, rooms, timeslots, conflicts, instructors = load_all_data()
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Make sure CSV files are in the current directory")
        return

    # Create CSP and get domains
    csp = TimetableCSP(courses, rooms, timeslots, conflicts, instructors)
    domains = csp.get_domain()

    # Show domain sizes
    print("\nInitial domain sizes:")
    for course_id, domain in domains.items():
        print(f"  {course_id}: {len(domain)} possible (time,room) pairs")
        if len(domain) == 0:
            print(f"    WARNING: No valid assignments for {course_id}!")

    # Run the selected algorithm
    algorithm_map = {
        "backtrack": "Backtracking Search",
        "forward": "Forward Checking",
        "mac": "MAC (Maintaining Arc Consistency)",
        "minconflicts": "Min-Conflicts Local Search"
    }

    solution, metrics = solve_with_algorithm(
        args.algorithm, courses, domains, conflicts
    )

    # Print results
    if solution:
        print_solution(algorithm_map[args.algorithm], solution, metrics,
                       courses, timeslots, rooms)
    else:
        print("\n" + "=" * 60)
        print("FAILED TO FIND A SOLUTION")
        print("=" * 60)
        print(f"Algorithm: {algorithm_map[args.algorithm]}")
        print("Try a different algorithm or generate a new instance")

        if metrics:
            print(f"\nAssignments made: {metrics.assignments}")
            print(f"Backtracks: {metrics.backtracks}")
            print(f"Time: {metrics.get_execution_time():.4f}s")


if __name__ == "__main__":
    main()