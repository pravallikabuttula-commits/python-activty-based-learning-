# Each classroom is a nested list of seats.
# None = vacant seat
# "RESERVED" = seat cannot be allocated
# Any other value = assigned student ID

classrooms = [
    ["S101", None, "RESERVED", "S102", None],   # Classroom 1
    [None, "S103", None, None, "RESERVED"],     # Classroom 2
    ["S104", None, "S101", None, None]          # Classroom 3 (duplicate S101)
]


def display_classrooms(classrooms):
    """Display classroom seating arrangement."""
    print("\nCLASSROOM SEATING")
    print("-" * 45)

    for room_number, seats in enumerate(classrooms, start=1):
        print(f"Classroom {room_number}: {seats}")


def find_duplicate_assignments(classrooms):
    """Find students allocated more than once."""
    assigned_students = {}
    duplicates = {}

    for room_number, seats in enumerate(classrooms, start=1):
        for seat_number, student in enumerate(seats, start=1):

            if student is not None and student != "RESERVED":
                position = f"Classroom {room_number}, Seat {seat_number}"

                if student in assigned_students:
                    if student not in duplicates:
                        duplicates[student] = [assigned_students[student]]

                    duplicates[student].append(position)
                else:
                    assigned_students[student] = position

    return duplicates


def calculate_vacant_capacity(classrooms):
    """Count total vacant seats and reserved seats."""
    vacant_seats = 0
    reserved_seats = 0
    occupied_seats = 0

    for seats in classrooms:
        for seat in seats:
            if seat is None:
                vacant_seats += 1
            elif seat == "RESERVED":
                reserved_seats += 1
            else:
                occupied_seats += 1

    return vacant_seats, reserved_seats, occupied_seats


def allocate_student(classrooms, student_id):
    """
    Allocate student to the first vacant seat.
    Reserved seats are preserved and never changed.
    """
    # Check whether student already has a seat
    for room_number, seats in enumerate(classrooms, start=1):
        if student_id in seats:
            return f"{student_id} is already assigned in Classroom {room_number}."

    # Find first vacant seat
    for room_number, seats in enumerate(classrooms, start=1):
        for seat_number, seat in enumerate(seats):
            if seat is None:
                seats[seat_number] = student_id
                return (
                    f"{student_id} allocated to Classroom {room_number}, "
                    f"Seat {seat_number + 1}."
                )

    return f"No vacant seat available for {student_id}."


# Display current layout
display_classrooms(classrooms)

# Allocate new students
print(allocate_student(classrooms, "S105"))
print(allocate_student(classrooms, "S106"))
print(allocate_student(classrooms, "S101"))  # Already assigned

# Check duplicate assignments
duplicates = find_duplicate_assignments(classrooms)

print("\nDUPLICATE ASSIGNMENTS")
print("-" * 45)

if duplicates:
    for student, positions in duplicates.items():
        print(f"{student} is assigned multiple times:")
        for position in positions:
            print("  -", position)
else:
    print("No duplicate assignments found.")

# Calculate capacity
vacant, reserved, occupied = calculate_vacant_capacity(classrooms)

print("\nOCCUPANCY SUMMARY")
print("-" * 45)
print("Occupied Seats:", occupied)
print("Vacant Seats:", vacant)
print("Reserved Seats:", reserved)
print("Total Seats:", occupied + vacant + reserved)

# Display final layout
display_classrooms(classrooms)