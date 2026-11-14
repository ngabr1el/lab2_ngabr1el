import csv

with open("grades.csv", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        score = float(row["score"])
        if score < 0 or score >100:
            print("Invalid score for", row["assignment"], ":", score)
