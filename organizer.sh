if [ ! -d "archive" ]; then
	mkdir archive
	echo "Created folder: archive"
fi

if [ ! -f "grades.csv" ]; then
	echo "Error: grades.csv was not found in this folder."
	echo "Run this script from the folder that contains grades.csv."
	exit 1
fi

timestamp=$(date +%Y%m%d-%H%M%S)
archived_name="grades_${timestamp}.csv"

if ! mv grades.csv "archive/$archived_name"; then
	echo "Error: could not move grades.csv into the archive folder."
	exit 1
fi

touch grades.csv 

echo "[$timestamp] Original: grades.csv | Archived as: archive/$archived_name" >> organizer.log

echo "Archived grades.csv as archive/$archived_name"
echo "Created a new empty grades.csv"
echo "Logged to organizer.log"

