from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Course:
    code: str
    teacher: str
    room: str
    # Example: ("Monday", "09:00", "10:30")
    schedule: Tuple[str, str, str]


def time_to_minutes(time_text: str) -> int:
    """Convert 'HH:MM' into total minutes."""
    hours, minutes = map(int, time_text.split(":"))
    return hours * 60 + minutes


def parse_schedule(schedule_text: str) -> Tuple[str, str, str]:
    """
    Convert a schedule string to a tuple.

    Input example:
    'Monday, 09:00-10:30'

    Output:
    ('Monday', '09:00', '10:30')
    """
    day, time_range = schedule_text.split(",")
    start_time, end_time = time_range.strip().split("-")
    return day.strip(), start_time.strip(), end_time.strip()


def schedules_overlap(schedule1: Tuple[str, str, str],
                      schedule2: Tuple[str, str, str]) -> bool:
    """Return True if two schedules overlap on the same day."""
    day1, start1, end1 = schedule1
    day2, start2, end2 = schedule2

    if day1.lower() != day2.lower():
        return False

    start1 = time_to_minutes(start1)
    end1 = time_to_minutes(end1)
    start2 = time_to_minutes(start2)
    end2 = time_to_minutes(end2)

    # Example: 09:00-10:00 and 09:30-11:00 overlap
    return start1 < end2 and start2 < end1


def find_conflicts(courses: List[Course]) -> List[str]:
    """Find teacher, room, and course timing conflicts."""
    conflicts = []

    for i in range(len(courses)):
        for j in range(i + 1, len(courses)):
            course1 = courses[i]
            course2 = courses[j]

            if schedules_overlap(course1.schedule, course2.schedule):

                if course1.room == course2.room:
                    conflicts.append(
                        f"Room conflict: {course1.room} is used by "
                        f"{course1.code} and {course2.code}."
                    )

                if course1.teacher == course2.teacher:
                    conflicts.append(
                        f"Teacher conflict: {course1.teacher} teaches "
                        f"{course1.code} and {course2.code} at the same time."
                    )

    return conflicts


def validate_proposed_course(proposed_course: Course,
                             existing_courses: List[Course],
                             unavailable_rooms: List[str]) -> List[str]:
    """Validate a newly proposed timetable entry."""
    errors = []

    if proposed_course.room in unavailable_rooms:
        errors.append(
            f"Room {proposed_course.room} is unavailable."
        )

    day, start, end = proposed_course.schedule

    if time_to_minutes(start) >= time_to_minutes(end):
        errors.append("Start time must be earlier than end time.")

    for course in existing_courses:
        if schedules_overlap(proposed_course.schedule, course.schedule):

            if proposed_course.room == course.room:
                errors.append(
                    f"Room {proposed_course.room} conflicts with "
                    f"{course.code}."
                )

            if proposed_course.teacher == course.teacher:
                errors.append(
                    f"Teacher {proposed_course.teacher} conflicts with "
                    f"{course.code}."
                )

    return errors


# Schedules as strings converted to tuples
math_schedule = parse_schedule("Monday, 09:00-10:30")
physics_schedule = parse_schedule("Monday, 10:00-11:30")
english_schedule = parse_schedule("Tuesday, 09:00-10:00")

courses = [
    Course("MAT101", "Dr. Kumar", "Room-101", math_schedule),
    Course("PHY101", "Dr. Singh", "Room-101", physics_schedule),
    Course("ENG101", "Dr. Kumar", "Room-202", english_schedule)
]

# Detect conflicts in current timetable
conflicts = find_conflicts(courses)

print("CURRENT TIMETABLE CONFLICTS")
print("-" * 40)

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts found.")

# Validate a new proposed course
proposed_course = Course(
    "CSC101",
    "Dr. Kumar",
    "Room-202",
    parse_schedule("Monday, 09:30-10:30")
)

unavailable_rooms = ["Room-303", "Lab-2"]

validation_errors = validate_proposed_course(
    proposed_course,
    courses,
    unavailable_rooms
)

print("\nPROPOSED TIMETABLE VALIDATION")
print("-" * 40)

if validation_errors:
    for error in validation_errors:
        print(error)
else:
    print("Proposed course is valid and can be added.")
    