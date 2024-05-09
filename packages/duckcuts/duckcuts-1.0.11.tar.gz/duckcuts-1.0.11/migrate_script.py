import csv
import sys
import json


def main():
    filename = sys.argv[1]
    print("Hello from migrate_script.py")
    print(f"Filename: {filename}")
    json_list = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            row_dict = {"action": row[0], "shortcut": row[1], "description": ""}
            json_list.append(row_dict)

    print(json_list)
    new_name = filename.replace(".csv", ".json")
    with open(new_name, "w") as file:
        file.write(json.dumps(json_list))


main()
