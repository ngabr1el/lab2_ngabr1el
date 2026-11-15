import csv

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
