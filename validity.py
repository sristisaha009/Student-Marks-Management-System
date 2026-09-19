import csv

def validate_faculty(faculty_id, password):
    """
    Validates faculty login credentials and returns faculty name if valid.
    """
    try:
        with open("Faculty DataBase.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["FacultyID"] == faculty_id and row["Password"] == password:
                    return row["Name"]  # Return faculty name instead of just True
        return None
    except FileNotFoundError:
        print("Error: Faculty DataBase.csv not found.")
        return None

def validate_student(enrollment, password):
    """
    Validates student login credentials and returns student details if valid.

    Args:
        enrollment (str): The enrollment number entered by the student.
        password (str): The password entered by the student.

    Returns:
        dict: A dictionary containing student details if login is successful, otherwise None.
    """
    try:
        with open("Student DataBase.csv", mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Enrollment"] == enrollment and row["Password"] == password:
                    # Return the student details as a dictionary
                    return row
        return None  # Return None if no matching student is found
    except FileNotFoundError:
        print("Error: Student DataBase.csv not found.")
        return None