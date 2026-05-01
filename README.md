# CSP University Timetabling Solver

This project solves a university timetable scheduling problem using Constraint Satisfaction Problem (CSP) techniques.

The goal is to assign each course a valid time slot and room while satisfying hard constraints such as room capacity, room features, instructor availability, student conflicts, and instructor clashes.

---

## Features

- Loads timetable data from CSV files  
- Generates valid domains for each course  
- Supports four CSP solving algorithms:
  - Backtracking Search  
  - Forward Checking  
  - MAC (Maintaining Arc Consistency)  
  - Min-Conflicts Local Search  
- Uses heuristics:
  - MRV (Minimum Remaining Values)  
  - Degree heuristic  
  - LCV (Least Constraining Value)  
- Prints timetable in readable format  
- Shows performance metrics  
- Can generate random test instances  
- Includes experiment support for comparing algorithms  

---

## Project Structure

Q_1/
├── main.py
├── csp.py
├── algorithms.py
├── heuristics.py
├── time_table.py
├── output_formatter.py
├── Performance.py
├── generator.py
├── experiments.py
├── debug.py
├── quick_fix.py
├── courses.csv
├── rooms.csv
├── timeslots.csv
├── students.csv
└── instructor_availability.csv

---

## Requirements

Install dependencies:

pip install pandas

---

## Input Files

- courses.csv → course details  
- rooms.csv → room details  
- timeslots.csv → available time slots  
- students.csv → enrollment data  
- instructor_availability.csv → instructor preferences  

---

## Constraints

1. No room conflict  
2. No instructor conflict  
3. No student conflict  
4. Room capacity must be sufficient  
5. Room must satisfy required features  
6. Timeslot duration must match course duration  
7. Instructor availability respected  

---

## Commands

Run default:

python main.py

Run specific algorithms:

python main.py --algorithm backtrack  
python main.py --algorithm forward  
python main.py --algorithm mac  
python main.py --algorithm minconflicts  

Run with custom input:

python main.py --input-dir instances/test --algorithm mac  

Generate test data:

python main.py --generate --courses 20 --rooms 16 --output-dir instances/my_test  

Run experiments:

python main.py --experiment 1  

---

## Output

- Algorithm used  
- Domain sizes  
- Final timetable  
- Grid schedule  
- Performance stats  

---

## Example

python main.py --algorithm mac
