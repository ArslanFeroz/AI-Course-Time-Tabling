# AI Course Timetabling Solver

An AI-based university course timetabling solver that models scheduling as a **Constraint Satisfaction Problem (CSP)**. It assigns courses to suitable rooms and time slots while checking hard constraints involving room capacity and features, instructor availability, and student/instructor clashes.

## Features

- Loads course, room, timeslot, student, and instructor-availability data from CSV files.
- Builds candidate domains for course assignments.
- Implements four solving approaches:
  - Backtracking Search
  - Forward Checking
  - Maintaining Arc Consistency (MAC), using AC-3
  - Min-Conflicts Local Search
- Includes variable/value-ordering heuristics:
  - Minimum Remaining Values (MRV)
  - Degree heuristic
  - Least Constraining Value (LCV)
- Generates configurable synthetic timetable instances.
- Runs experiments to compare search strategies and heuristics.
- Reports solution information and performance metrics.

## Constraints Modelled

The solver checks constraints including:

- A room cannot host overlapping courses.
- An instructor cannot teach overlapping courses.
- Students cannot be scheduled into conflicting courses.
- Room capacity must satisfy course enrolment.
- Room features must meet course requirements.
- Instructor availability must be respected.
- Course duration must fit the selected time slot.

## Algorithms at a Glance

| Algorithm | Purpose |
|---|---|
| Backtracking | Builds an assignment incrementally and backtracks on conflicts. |
| Forward Checking | Removes values from neighbouring domains after an assignment. |
| MAC / AC-3 | Maintains arc consistency as assignments are made. |
| Min-Conflicts | Uses local search to reduce conflicts in a complete assignment. |

The project also includes heuristics to choose which course to assign next and which candidate assignment to try first.

## Technology Stack

- Python 3
- pandas
- Constraint Satisfaction Problems
- Search and local-search algorithms
- CSV-based input datasets

## Repository Structure

```text
AI-Course-Time-Tabling/
├── main.py
├── csp.py
├── algorithms.py
├── heuristics.py
├── time_table.py
├── output_formatter.py
├── Performance.py
├── generator.py
├── experiments.py
├── courses.csv
└── instances/              # Example generated/input instances
```

## Setup

```bash
git clone https://github.com/ArslanFeroz/AI-Course-Time-Tabling.git
cd AI-Course-Time-Tabling

python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

Install the dependency:

```bash
python -m pip install --upgrade pip
pip install pandas
```

## Usage

Run the default solver (MAC is the default algorithm):

```bash
python main.py
```

Choose an algorithm:

```bash
python main.py --algorithm backtrack
python main.py --algorithm forward
python main.py --algorithm mac
python main.py --algorithm minconflicts
```

Use a different input directory:

```bash
python main.py --input-dir instances/exp1_1 --algorithm mac
```

Generate a test instance:

```bash
python main.py --generate --courses 20 --rooms 16 --output-dir instances/my_test
```

Run an experiment:

```bash
python main.py --experiment 1
```

The command-line interface supports experiments 1 through 4.

## Input Data

The input data is CSV-based. The project uses files for:

- Courses
- Rooms
- Time slots
- Students/enrolments
- Instructor availability

When supplying a custom instance, ensure the expected CSV files and column formats are present in the selected input directory.

## Output

The program prints the selected algorithm, timetable assignment information, a readable schedule, and performance measurements collected by the project.

## Learning Outcomes

This project explores CSP modelling, domain construction, constraint propagation, heuristic search, local search, synthetic test generation, and empirical comparison of AI algorithms.


