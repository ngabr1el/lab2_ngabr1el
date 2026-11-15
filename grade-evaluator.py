import csv

failed_names = []
failed_weights = []
formative_weight = 0
summative_weight = 0
formative_points = 0
summative_points = 0

with open("grades.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        score = float(row["score"])
        weight = float(row["weight"])
        points = score * weight / 100

        if score < 0 or score > 100:
            print("Invalid score for", row["assignment"], ":", score)

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
            print("Unknown group for", row["assignment"], ":", row["group"])

total_weight = formative_weight + summative_weight
print("Formative weight:", formative_weight)
print("Summative weight:", summative_weight)
print("Total weight:", total_weight)

if formative_weight != 60:
    print("Error: Formative weights must add up to 60, but they add up to", formative_weight)
if summative_weight != 40:
    print("Error: Summative weights must add up to 40, but they add up to", summative_weight)
if total_weight != 100:
    print("Error: Total weight must be exactly 100, but it is", total_weight)

total_grade = formative_points + summative_points
gpa = (total_grade / 100) * 5.0
print("Formative points:", formative_points)
print("Summative points:", summative_points)
print("Total grade:", total_grade)
print("GPA:", gpa)


formative_percent = formative_points / 60 * 100
summative_percent = summative_points / 40 * 100
print("Formative percent:", formative_percent)
print("Summative percent:", summative_percent)

if formative_percent >= 50 and summative_percent >= 50:
    print("Final status: PASSED")
else:
    print("Final status: FAILED")


if len(failed_names) == 0:
    print("No formative assignments to resubmit.")
else:
    highest = max(failed_weights)
    print("Eligible for resubmission:")
    for i in range(len(failed_names)):
        if failed_weights[i] == highest:
            print("-", failed_names[i])
