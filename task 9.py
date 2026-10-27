def analyze_student_id(student_id):
    """
    Expected ID format:
    YYYY-BRANCH-ROLL

    Example:
    2024-CSE-101

    YYYY   = Admission year
    BRANCH = CSE, ECE, ME, CIVIL, IT
    ROLL   = 3-digit student roll number
    """
    student_id = student_id.strip()

    valid_branches = {
        "CSE": "Computer Science Engineering",
        "ECE": "Electronics and Communication Engineering",
        "ME": "Mechanical Engineering",
        "CIVIL": "Civil Engineering",
        "IT": "Information Technology"
    }

    parts = student_id.split("-")

    # Validate number of sections
    if len(parts) != 3:
        return None, "Invalid format. Use YYYY-BRANCH-ROLL."

    admission_year = parts[0]
    branch_code = parts[1].upper()
    roll_number = parts[2]

    # Validate admission year
    if not admission_year.isdigit() or len(admission_year) != 4:
        return None, "Admission year must contain 4 digits."

    year = int(admission_year)

    if year < 2000 or year > 2030:
        return None, "Admission year is outside the valid range."

    # Validate branch code
    if branch_code not in valid_branches:
        return None, "Invalid branch code."

    # Validate roll number
    if not roll_number.isdigit() or len(roll_number) != 3:
        return None, "Roll number must contain exactly 3 digits."

    # Classify admission type using year
    if year >= 2025:
        admission_category = "Current Admission Batch"
    elif year >= 2021:
        admission_category = "Recent Admission Batch"
    else:
        admission_category = "Earlier Admission Batch"

    return {
        "student_id": student_id,
        "admission_year": year,
        "branch_code": branch_code,
        "branch_name": valid_branches[branch_code],
        "roll_number": roll_number,
        "admission_category": admission_category
    }, None


def process_student_ids(student_ids):
    for student_id in student_ids:
        result, error = analyze_student_id(student_id)

        print("-" * 50)
        print("Student ID:", student_id)

        if error:
            print("Status: Invalid")
            print("Reason:", error)
        else:
            print("Status:", "Valid")
            print("Admission Year:", result["admission_year"])
            print("Branch Code:", result["branch_code"])
            print("Branch Name:", result["branch_name"])
            print("Roll Number:", result["roll_number"])
            print("Classification:", result["admission_category"])


# Sample student identification strings
student_ids = [
    "2024-CSE-101",
    "2025-ECE-205",
    "2022-IT-055",
    "2019-ME-120",
    "2024-CSE-12",       # Invalid roll number
    "2024-ABC-100",      # Invalid branch
    "20A4-CIVIL-300",    # Invalid year
    "2024-CSE-101-55"    # Invalid format
]

process_student_ids(student_ids)