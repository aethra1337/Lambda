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
# 2. SUPPORTING CLASSES & EXAM SYSTEM
# ==========================================
class Classroom:
    def __init__(self, room_number: str, capacity: int):
        self.room_number: str = room_number
        self.capacity: int = capacity


class Exam:
    def __init__(self, exam_type: str, weight: float):
        self.exam_type: str = exam_type  # e.g., "Midterm", "Final", "Quiz", "Project"
        self.weight: float = weight      # Percentage weight (e.g., 0.30 for 30%)
        self.score: float = 0.0          # Default score before grading

    def set_score(self, score: float) -> None:
        self.score = score


class Department:
    def __init__(self, department_id: int, department_name: str):
        self.department_id: int = department_id
        self.department_name: str = department_name
        self.teachers: List['Teacher'] = []
        self.course_catalog: List['Subject'] = []  # Available courses in this department

    def add_teacher(self, teacher: 'Teacher') -> None:
        self.teachers.append(teacher)

    def add_to_catalog(self, subject: 'Subject') -> None:
        self.course_catalog.append(subject)

    def show_catalog(self) -> None:
        print(f"\n--- Course Catalog for {self.department_name} ---")
        for subject in self.course_catalog:
            teacher_name = subject.teacher._name if subject.teacher else "TBA"
            print(f" * [{subject.subject_code}] {subject.subject_name} ({subject.credits} Credits) - Instructor: {teacher_name}")
        print("-" * 50)


# ==========================================
# 3. CORE BUSINESS CLASSES (Subject & Enrollment)
# ==========================================
class Subject:
    def __init__(self, subject_code: str, subject_name: str, credits: int, classroom: Classroom):
        self.subject_code: str = subject_code
        self.subject_name: str = subject_name
        self.credits: int = credits
        self.classroom: Classroom = classroom
        self.teacher: Optional['Teacher'] = None
        self.exam_structures: List[Exam] = []  # Defined exams for this course

    def assign_teacher(self, teacher: 'Teacher') -> None:
        self.teacher = teacher

    def add_exam_structure(self, exam_type: str, weight: float) -> None:
        """Defines what exams this course will have (e.g., Midterm 30%, Final 70%)."""
        self.exam_structures.append(Exam(exam_type, weight))


class Enrollment:
    def __init__(self, enrollment_id: int, student: 'Student', subject: Subject):
        self.enrollment_id: int = enrollment_id
        self.student: 'Student' = student
        self.subject: Subject = subject
        # Clone the exam structures from the subject specifically for this student's instance
        self.my_exams: List[Exam] = [Exam(e.exam_type, e.weight) for e in subject.exam_structures]

    def grade_exam(self, exam_type: str, score: float) -> None:
        """Finds the specific exam type and assigns a score to it."""
        for exam in self.my_exams:
            if exam.exam_type == exam_type:
                exam.set_score(score)
                return
        print(f"Warning: Exam type '{exam_type}' not found in {self.subject.subject_name}.")

    def calculate_average(self) -> float:
        total_average = 0.0
        for exam in self.my_exams:
            total_average += exam.score * exam.weight
        return total_average

    def get_letter_grade(self) -> str:
        avg = self.calculate_average()
        if avg >= 90: return "AA"
        elif avg >= 85: return "BA"
        elif avg >= 80: return "BB"
        elif avg >= 70: return "CB"
        elif avg >= 60: return "CC"
        else: return "FF"


# ==========================================
# 4. INHERITED CLASSES (Student & Teacher)
# ==========================================
class Student(Person):
    def __init__(self, person_id: int, name: str, email: str, enrollment_date: date):
        super().__init__(person_id, name, email)
        self.enrollment_date: date = enrollment_date
        self.selected_courses: List[Enrollment] = []  # Dynamic course selection list

    def select_course(self, enrollment_id: int, subject: Subject) -> Optional[Enrollment]:
        """Allows the student to dynamically register/select a course from the catalog."""
        # Check if already enrolled
        for enc in self.selected_courses:
            if enc.subject.subject_code == subject.subject_code:
                print(f"{self._name} is already registered for {subject.subject_name}.")
                return None
        
        new_enrollment = Enrollment(enrollment_id, self, subject)
        self.selected_courses.append(new_enrollment)
        print(f"[SUCCESS] {self._name} successfully registered for: {subject.subject_name}")
        return new_enrollment

    def show_info(self) -> None:
        print(f"\n--- Student Report Card ---")
        print(f"ID: {self._id} | Name: {self._name} | Email: {self._email}")
        print(f"Registration Date: {self.enrollment_date}")
        print(f"Selected Courses & Performance Details:")
        if not self.selected_courses:
            print("  No courses selected yet.")
        else:
            for enc in self.selected_courses:
                print(f"  > [{enc.subject.subject_code}] {enc.subject.subject_name}:")
                # Show breakdown of each exam score
                exam_details = ", ".join([f"{e.exam_type}: {e.score} (w: {int(e.weight*100)}%)" for e in enc.my_exams])
                print(f"    Breakdown -> {exam_details}")
                print(f"    Final Status -> Average: {enc.calculate_average():.2f} | Grade: {enc.get_letter_grade()}")
        print("-" * 30)


class Teacher(Person):
    def __init__(self, person_id: int, name: str, email: str, hire_date: date, salary: float):
        super().__init__(person_id, name, email)
        self.hire_date: date = hire_date
        self.salary: float = salary
        self.taught_subjects: List[Subject] = []

    def assign_to_subject(self, subject: Subject) -> None:
        self.taught_subjects.append(subject)
        subject.assign_teacher(self)

    def show_info(self) -> None:
        print(f"\n--- Instructor Profile ---")
        print(f"ID: {self._id} | Name: {self._name}")
        print(f"Active Active Courses: " + ", ".join([s.subject_name for s in self.taught_subjects]))
        print("-" * 30)


# ==========================================
# 5. SIMULATION CONTROL FLOW
# ==========================================
if __name__ == "__main__":
    print("=== Advanced School Management System Initialized ===\n")

    # 1. Create Infrastructure & Department
    lab_101 = Classroom("Lab 101", 30)
    hall_A = Classroom("Lecture Hall A", 80)
    cloud_dept = Department(10, "Cloud Computing Operations Department")

    # 2. Create Faculty Members
    instructor_1 = Teacher(501, "Andrzej Pieczonka ", "andrzejpieczonka@pans.edu.pl", date(2021, 2, 15), 52000.0)
    instructor_2 = Teacher(502, "Marek Zarychta", "marekzarychta@pans.edu.pl", date(2019, 9, 1), 60000.0)
    cloud_dept.add_teacher(instructor_1)
    cloud_dept.add_teacher(instructor_2)

    # 3. Create Multiple Subjects & Setup Custom Exam Structures
    # Course A: Has Midterm, Quiz, and Final
    course_python = Subject("PANS-101", "Advanced Python & Automation", 4, lab_101)
    course_python.add_exam_structure("Midterm", 0.30)
    course_python.add_exam_structure("Quiz", 0.10)
    course_python.add_exam_structure("Final", 0.60)
    instructor_1.assign_to_subject(course_python)

    # Course B: Has Project and Final only
    course_cloud = Subject("PANS-202", "Cloud Infrastructure & Operations", 5, hall_A)
    course_cloud.add_exam_structure("Project", 0.40)
    course_cloud.add_exam_structure("Final", 0.60)
    instructor_2.assign_to_subject(course_cloud)

    # Add courses to department catalog
    cloud_dept.add_to_catalog(course_python)
    cloud_dept.add_to_catalog(course_cloud)

    # Display available courses
    cloud_dept.show_catalog()

    # 4. Create Student Instance
    student_1 = Student(20260001, "Ahmet Talha", "ahmet.talha@pans.edu.pl", date(2025, 9, 10))

    print("\n--- Student Registration Phase ---")
    # Student selects courses from the catalog dynamically
    reg_python = student_1.select_course(enrollment_id=9001, subject=course_python)
    reg_cloud = student_1.select_course(enrollment_id=9002, subject=course_cloud)

    # 5. Instructor Inputs Grades for Exams
    print("\n--- Academic Grading Phase ---")
    if reg_python:
        reg_python.grade_exam("Midterm", 85.0)
        reg_python.grade_exam("Quiz", 90.0)
        reg_python.grade_exam("Final", 78.0)

    if reg_cloud:
        reg_cloud.grade_exam("Project", 95.0)
        reg_cloud.grade_exam("Final", 88.0)
    
    print("[INFO] All exam entries completed by instructors.")

    # 6. Display Final System Diagnostics Output
    student_1.show_info()
    instructor_1.show_info()