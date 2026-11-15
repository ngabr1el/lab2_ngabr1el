import csv
import os
import sys

filename = input("Enter the name of the CSV file (e.g., grades.csv): ").strip()
if filename == "":
    filename = "grades.csv"

if not os.path.exists(filename):
    print("Error: the file", filename, "was not found.")
    print("Make sure it is in the same folder as this program and the name is spelled correctly (e.g., grades.csv).")
    sys.exit()

if os.path.getsize(filename) == 0:
    print("Error: the file", filename, "is empty.")
    print("It should start with a header row (e.g., assignment,group,score,weight) followed by your grades.")
    sys.exit()

failed_names = []
failed_weights = []
errors = []
transcript_lines = []
formative_weight = 0
summative_weight = 0
formative_points = 0
summative_points = 0

with open(filename, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        name = row["assignment"]
        if name is None or name.strip() == "":
            print("Skipping row on line", reader.line_num, "because it is empty or has no assignment name.")
            continue

        try:
            score = float(row["score"])
            weight = float(row["weight"])
        except (ValueError, TypeError):
            errors.append("Line " + str(reader.line_num) + " (" + name + "): score and weight must be numbers, for example 85 and 20.")
            continue

        points = score * weight / 100

        if score < 0 or score > 100:
            errors.append("Line " + str(reader.line_num) + " (" + name + "): score " + row["score"] + " must be between 0 and 100, for example 85.")
            continue

        if row["group"] == "Formative":
            formative_weight = formative_weight + weight
            formative_points = formative_points + points
            if score < 50:
                failed_names.append(row["assignment"])
                failed_weights.append(weight)
        elif row["group"] == "Summative":
            summative_weight = summative_weight + weight
            summative_points = summative_points + points
        else:
            errors.append("Line " + str(reader.line_num) + " (" + name + "): group must be Formative or Summative, but it is '" + row["group"] + "'.")

        transcript_lines.append(name.ljust(38) + row["group"].ljust(12) + str(score).rjust(7) + str(weight).rjust(8) + str(round(points, 2)).rjust(8))
total_weight = formative_weight + summative_weight

if len(errors) == 0:
    if formative_weight != 60:
        errors.append("Formative weights must add up to 60, but they add up to " + str(formative_weight) + ".")
    if summative_weight != 40:
        errors.append("Summative weights must add up to 40, but they add up to " + str(summative_weight) + ".")
    if total_weight != 100:
        errors.append("The total weight must be exactly 100, but it is " + str(total_weight) + ".")

if len(errors) > 0:
    print("Cannot generate the transcript. Problems found in", filename, ":")
    for message in errors:
        print("-", message)
    sys.exit()


total_grade = formative_points + summative_points
gpa = (total_grade / 100) * 5.0
formative_percent = formative_points / 60 * 100
summative_percent = summative_points / 40 * 100

print("")
print("=" * 73)
print("AFRICAN LEADERSHIP UNIVERSITY - STUDENT TRANSCRIPT")
print("=" * 73)
print("Assignment".ljust(38) + "Group".ljust(12) + "Score".rjust(7) + "Weight".rjust(8) + "Points".rjust(8))
print("-" * 73)
for line in transcript_lines:
    print(line)
print("-" * 73)
print("Formative:", round(formative_points, 2), "/ 60 (" + str(round(formative_percent, 1)) + "%)")
print("Summative:", round(summative_points, 2), "/ 40 (" + str(round(summative_percent, 1)) + "%)")
print("Total grade:", round(total_grade, 2), "/ 100")
print("GPA:", round(gpa, 2), "/ 5.0")

if formative_percent >= 50 and summative_percent >= 50:
    print("Final status: PASSED")
else:
    print("Final status: FAILED")

print("-" * 73)
if len(failed_names) == 0:
    print("No formative assignments to resubmit.")
else:
    highest = max(failed_weights)
    print("Eligible for resubmission:")
    for i in range(len(failed_names)):
        if failed_weights[i] == highest:
            print("-", failed_names[i])
print("=" * 73)
