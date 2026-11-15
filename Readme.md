# ALU Transcript Generator

A Python program that reads a CSV file of course grades and prints a student transcript with the GPA, a PASSED/FAILED status and the assignment(s) to resubmit. A Bash script archives each batch of grades and keeps a log.

Course: Introduction to Python Programming and Databases (Individual Coding Lab, Lab 2)
Author: ngabr1el

## Files

| File | Purpose |
|------|---------|
| `grade-evaluator.py` | The Python program: validates the data, calculates the GPA, decides PASSED/FAILED and lists resubmissions |
| `organizer.sh` | The Bash script: archives `grades.csv` with a timestamp, creates a fresh `grades.csv` and writes `organizer.log` |
| `grades.csv` | The grades data |
| `Readme.md` | This file |

## Requirements

Python 3 and Bash. Nothing else needs to be installed.

## CSV format

The first line is a header row, followed by one line per assignment:

```
assignment,group,score,weight
Quiz,Formative,85,20
Midterm Project - Simple Calculator,Summative,70,20
```

- `group` must be `Formative` or `Summative`
- `score` is a number from 0 to 100
- `weight` is a number; all weights must add up to 100 (Formative 60, Summative 40)

## How to run

```
python3 grade-evaluator.py
```

The program asks for the CSV file name (for example `grades.csv`). Press Enter to use `grades.csv`.

```
bash organizer.sh
```

Warning: `organizer.sh` moves `grades.csv` into the `archive` folder and leaves an empty `grades.csv` behind, so run it only when you want to archive the current batch of grades.

## What grade-evaluator.py does

1. Checks that the file exists and is not empty.
2. Converts scores and weights to numbers and checks that every score is between 0 and 100.
3. Checks that all weights add up to exactly 100, with Formative at 60 and Summative at 40.
4. Calculates the points for each assignment as score x weight / 100. The total grade is the sum of all points (out of 100).
5. Calculates the GPA with the formula GPA = (total grade / 100) x 5.0.
6. Decides the final status. A student is PASSED only if they score at least 50% in BOTH categories (Formative out of 60 and Summative out of 40). Otherwise the status is FAILED.
7. Finds the assignment(s) to resubmit: among the failed Formative assignments (score below 50), the one with the highest weight. If several share the highest weight, all of them are listed.

## Error handling

The program stops with a clear message, including the line number and an example, instead of crashing, for:

- a missing file
- an empty file
- empty rows (they are skipped with a notice)
- scores or weights that are not numbers
- scores outside the range 0 to 100
- a group that is not Formative or Summative
- weights that do not add up to 100 (Formative 60, Summative 40)

Example:

```
Cannot generate the transcript. Problems found in grades.csv :
- Line 2 (Quiz): score 105 must be between 0 and 100, for example 85.
```

## Sample output

Using the provided `grades.csv`:

```
=========================================================================
AFRICAN LEADERSHIP UNIVERSITY - STUDENT TRANSCRIPT
=========================================================================
Assignment                            Group         Score  Weight  Points
-------------------------------------------------------------------------
Quiz                                  Formative      85.0    20.0    17.0
Group Exercise                        Formative      40.0    20.0     8.0
Functions and Debugging Lab           Formative      45.0    20.0     9.0
Midterm Project - Simple Calculator   Summative      70.0    20.0    14.0
Final Project - Text-Based Game       Summative      60.0    20.0    12.0
-------------------------------------------------------------------------
Formative: 34.0 / 60 (56.7%)
Summative: 26.0 / 40 (65.0%)
Total grade: 60.0 / 100
GPA: 3.0 / 5.0
Final status: PASSED
-------------------------------------------------------------------------
Eligible for resubmission:
- Group Exercise
- Functions and Debugging Lab
=========================================================================
```

Group Exercise and Functions and Debugging Lab both failed (below 50) and share the highest failed weight (20), so both are eligible for resubmission.

## What organizer.sh does

1. Creates the `archive` folder if it does not exist.
2. Stops with an error message if `grades.csv` is not found.
3. Moves `grades.csv` into `archive` and renames it with a timestamp, for example `grades_20261115-154259.csv`.
4. Creates a new, empty `grades.csv`, ready for the next batch of grades.
5. Appends a line to `organizer.log` with the timestamp, the original file name and the archived file name. The log keeps the entries from every run.

Example log line:

```
[20261115-154259] Original: grades.csv | Archived as: archive/grades_20261115-154259.csv
```

## Libraries

Only Python's built-in modules are used: `csv` (to read the file), `os` (to check that the file exists and is not empty) and `sys` (to stop the program with `sys.exit()`). No external packages are used, and all the grading logic (validation, GPA, pass/fail and resubmission) is written by hand.

## Assumptions

- A failed assignment is one with a score below 50.
- Resubmission candidates are shown whenever a Formative assignment has failed, whatever the final status.
- Scores and weights are read as decimal numbers, so values like 85.5 are accepted.
