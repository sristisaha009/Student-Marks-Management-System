import csv
from docx import Document
import os

def extract_student_data_from_word(file_path):
    """
    Extracts student data from a Word file and returns a list of dictionaries.

    Args:
        file_path (str): Path to the Word file.

    Returns:
        list: A list of dictionaries containing student data.
    """
    students = []
    try:
        # Load the Word document
        doc = Document(file_path)

        # Iterate through paragraphs in the document
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text.startswith("Roll:"):
                # Extract student data
                student_data = {}
                for line in text.split(", "):
                    key, value = line.split(": ")
                    student_data[key] = value

                # Append the student data to the list
                students.append(student_data)

        return students
    except Exception as e:
        print(f"Error reading Word file: {e}")
        return []

def append_students_to_csv(students, csv_file_path):
    """
    Appends student data to the Student DataBase.csv file.

    Args:
        students (list): List of dictionaries containing student data.
        csv_file_path (str): Path to the Student DataBase.csv file.
    """
    try:
        # Read existing data to ensure the new data doesn't duplicate entries
        existing_enrollments = set()
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_enrollments.add(row["Enrollment"])

        # Append new students to the CSV file
        with open(csv_file_path, mode="a", newline="") as file:
            fieldnames = ["Roll", "Name", "Enrollment", "Password", "Sex", "DSA", "AC", "DC", "MATLAB"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for student in students:
                if student["Enrollment"] not in existing_enrollments:
                    writer.writerow({
                        "Roll": student["Roll"],
                        "Name": student["Name"],
                        "Enrollment": student["Enrollment"],
                        "Password": student["Password"],
                        "Sex": student["Sex"],
                        "DSA": student["DSA"],
                        "AC": student["AC"],
                        "DC": student["DC"],
                        "MATLAB": student["MATLAB"]
                    })
                    existing_enrollments.add(student["Enrollment"])
                    print(f"Added student: {student['Name']}")
                else:
                    print(f"Student with enrollment {student['Enrollment']} already exists.")

        # Sort the CSV file after appending new data
        csv_sorter(csv_file_path)
    except Exception as e:
        print(f"Error appending to CSV file: {e}")

def csv_sorter(csv_file_path):
    """
    Sorts the Student DataBase.csv file based on the "Enrollment" column.

    Args:
        csv_file_path (str): Path to the Student DataBase.csv file.
    """
    try:
        # Read the CSV file
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        # Sort rows by the "Enrollment" column
        rows.sort(key=lambda x: x["Enrollment"])

        # Write the sorted data back to the CSV file
        with open(csv_file_path, mode="w", newline="") as file:
            fieldnames = ["Roll", "Name", "Enrollment", "Password", "Sex", "DSA", "AC", "DC", "MATLAB"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print("CSV file sorted successfully.")
    except Exception as e:
        print(f"Error sorting CSV file: {e}")

# Example usage
if __name__ == "__main__":
    word_file_path = "students.docx"  # Path to the Word file
    csv_file_path = "Student DataBase.csv"  # Path to the CSV file

    students = extract_student_data_from_word(word_file_path)
    if students:
        append_students_to_csv(students, csv_file_path)