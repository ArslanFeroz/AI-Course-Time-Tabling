# Performance.py - Keeps track of how well our algorithms are doing

import time


class Metrics:
    """
    Simple metrics tracker.
    Counts assignments, backtracks, and constraint checks.
    Also tracks execution time.
    """

    def __init__(self):
        self.assignments = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.start_time = 0
        self.end_time = 0

    def start_timer(self):
        """Call this before running the algorithm"""
        self.start_time = time.time()

    def stop_timer(self):
        """Call this after the algorithm finishes"""
        self.end_time = time.time()

    def add_assignment(self):
        """Count one variable assignment"""
        self.assignments += 1

    def add_backtrack(self):
        """Count one backtrack (dead end)"""
        self.backtracks += 1

    def add_constraint_check(self):
        """Count one constraint check"""
        self.constraint_checks += 1

    def get_execution_time(self):
        """Get elapsed time in seconds"""
        return self.end_time - self.start_time

    def print_report(self, algorithm_name):
        """Print a nice formatted report"""
        print(f"\n{'=' * 50}")
        print(f"PERFORMANCE REPORT: {algorithm_name}")
        print(f"{'=' * 50}")
        print(f"Total Assignments:    {self.assignments}")
        print(f"Total Backtracks:     {self.backtracks}")
        print(f"Constraint Checks:    {self.constraint_checks}")
        print(f"Execution Time:       {self.get_execution_time():.4f} seconds")
        print(f"{'=' * 50}")

    def reset(self):
        """Reset all counters (for running multiple algorithms)"""
        self.assignments = 0
        self.backtracks = 0
        self.constraint_checks = 0
        self.start_time = 0
        self.end_time = 0