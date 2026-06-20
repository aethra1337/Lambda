from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


# ==========================================
# 1. ABSTRACT BASE CLASS
# ==========================================
class Person(ABC):
    def __init__(self, person_id: int, name: str, email: str):
        self._id: int = person_id
        self._name: str = name
        self._email: str = email

    @abstractmethod
    def show_info(self) -> None:
        """Each subclass must override this method."""
        pass


# ==========================================
# 2. SUPPORTING CLASSES
# ==========================================
class Classroom:
    def __init__(self, room_number: str, capacity: int):
        self.room_number: str = room_number
        self.capacity: int = capacity

    def is_available(self) -> bool:
        return True


class Department:
    def __init__(self, department_id: int, department_name: str):
        self.department_id: int = department_id
        self.department_name: str = department_name
        self.teachers: List['Teacher'] = []
        self.subjects: List['Subject'] = []

    def add_teacher(self, teacher: 'Teacher') -> None:
        self.teachers.append(teacher)

    def add_subject(self, subject: 'Subject') -> None:
        self.subjects.append(subject)

    def show_department_info(self) -> None:
        print(f"Department: {self.department_name} (Teachers: {len(self.teachers)}, Courses Offered: {len(self.subjects)})")


# ==========================================
# 3. CORE BUSINESS CLASSES
# ==========================================
class Subject:
    def __init__(self, subject_code: str, subject_name: str, credits: int, classroom: Classroom):
        self.subject_code: str = subject_code
        self.subject_name: str = subject_name
        self.credits: int = credits
        self.classroom: Classroom = classroom
        self.teacher: Optional['Teacher'] = None

    def assign_teacher(self, teacher: 'Teacher') -> None:
        self.teacher = teacher

    def show_subject(self) -> None:
        teacher_name = self.teacher._name if self.teacher else "Not Assigned"
        print(f"[{self.subject_code}] {self.subject_name} ({self.credits} Credits) | Room: {self.classroom.room_number} | Instructor: {teacher_name}")


class Enrollment:
    def __init__(self, enrollment_id: int, student: 'Student', subject: Subject):
        self.enrollment_id: int = enrollment_id
        self.student: 'Student' = student
        self.subject: Subject = subject
        self._exam1: float = 0.0
        self._exam2: float = 0.0
        self._final_exam: float = 0.0
        self.letter_grade: str = "F"

    def assign_grades(self, ex1: float, ex2: float, final: float) -> None:
        self._exam1 = ex1
        self._exam2 = ex2
        self._final_exam = final
        self.letter_grade = self.calculate_letter_grade()

    def calculate_average(self) -> float:
        # Weight formula: 30% Midterm 1, 30% Midterm 2, 40% Final Exam
        return (self._exam1 * 0.3) + (self._exam2 * 0.3) + (self._final_exam * 0.4)

    def calculate_letter_grade(self) -> str:
        avg = self.calculate_average()
        if avg >= 90: return "AA"
        elif avg >= 80: return "BA"
        elif avg >= 70: return "BB"
        elif avg >= 60: return "CB"
        elif avg >= 50: return "CC"
        else: return "FF"


# ==========================================
# 4. INHERITED CLASSES
# ==========================================
class Student(Person):
    def __init__(self, person_id: int, name: str, email: str, enrollment_date: date):
        super().__init__(person_id, name, email)
        self.enrollment_date: date = enrollment_date
        self.enrollments: List[Enrollment] = []

    def study(self) -> None:
        print(f"{self._name} is currently studying...")

    def enroll_in_subject(self, enrollment_id: int, subject: Subject) -> Enrollment:
        new_enrollment = Enrollment(enrollment_id, self, subject)
        self.enrollments.append(new_enrollment)
        return new_enrollment

    def show_info(self) -> None:
        print(f"--- Student Information ---")
        print(f"ID: {self._id} | Name: {self._name} | Email: {self._email}")
        print(f"Enrollment Date: {self.enrollment_date}")
        if self.enrollments:
            print("Enrolled Courses & Grades:")
            for enc in self.enrollments:
                print(f"  - {enc.subject.subject_name}: Average: {enc.calculate_average():.2f} ({enc.letter_grade})")
        print("---------------------------")


class Teacher(Person):
    def __init__(self, person_id: int, name: str, email: str, hire_date: date, salary: float):
        super().__init__(person_id, name, email)
        self.hire_date: date = hire_date
        self.salary: float = salary
        self.taught_subjects: List[Subject] = []

    def teach(self) -> None:
        print(f"{self._name} is currently teaching a lesson...")

    def assign_to_subject(self, subject: Subject) -> None:
        self.taught_subjects.append(subject)
        subject.assign_teacher(self)

    def show_info(self) -> None:
        print(f"--- Instructor Information ---")
        print(f"ID: {self._id} | Name: {self._name} | Email: {self._email}")
        print(f"Hire Date: {self.hire_date} | Courses Taught: {len(self.taught_subjects)}")
        print("-------------------------------")


# ==========================================
# 5. EXECUTION / SIMULATION FLOW
# ==========================================
if __name__ == "__main__":
    print("=== School Management System Initialized ===\n")

    # 1. Setup Infrastructure
    lab_101 = Classroom("Lab 101", 30)
    tech_department = Department(1, "Computer Technologies Department")

    # 2. Setup Faculty
    teacher_1 = Teacher(101, "John Doe", "john.doe@university.edu", date(2020, 9, 1), 45000.0)
    tech_department.add_teacher(teacher_1)

    # 3. Setup Course and Assign Instructor
    python_course = Subject("BPR101", "Python Programming", 4, lab_101)
    tech_department.add_subject(python_course)
    teacher_1.assign_to_subject(python_course)

    # 4. Setup Student and Process Enrollment
    student_1 = Student(2026001, "Alice Smith", "alice.smith@student.edu", date(2025, 9, 15))
    enrollment_record = student_1.enroll_in_subject(enrollment_id=5001, subject=python_course)

    # 5. Input Academic Performance
    # Midterm1: 75, Midterm2: 80, Final: 85
    enrollment_record.assign_grades(75.0, 80.0, 85.0)

    # 6. Display System Output Verification
    tech_department.show_department_info()
    python_course.show_subject()
    print()
    
    student_1.show_info()
    print()
    teacher_1.show_info()
    
    print("\nActions Execution:")
    student_1.study()
    teacher_1.teach()