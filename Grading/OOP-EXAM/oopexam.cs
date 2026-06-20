using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;

namespace SchoolSystemApp
{
    // Base abstract class for shared person attributes
    abstract class Person
    {
        public string FullName { get; set; }
        public int Age { get; set; }
        public string Department { get; set; }

        public abstract void Info();
    }

    class Student : Person
    {
        public string StudentId { get; set; }
        public int Score { get; set; }
        
        private static int totalStudents = 0;
        protected static Random random = new Random();

        public Student(string name, string id, string dept)
        {
            FullName = name;
            StudentId = id;
            Department = dept;
            Age = random.Next(18, 26);
            Score = random.Next(4, 16);
            totalStudents++;
        }

        // Empty constructor for generating random students
        public Student()
        {
            Department = GetRandomDepartment();
            Age = random.Next(18, 26);
            Score = random.Next(4, 16);
            totalStudents++;
        }

        public static int GetStudentCount() => totalStudents;

        public static string GenerateIdSuffix() => random.Next(100, 999).ToString();

        public void CreateIdPool(List<string> pool, int size)
        {
            while (pool.Count < size)
            {
                string suffix = GenerateIdSuffix();
                if (!pool.Contains(suffix))
                {
                    pool.Add(suffix);
                }
            }
        }

        private string GetRandomDepartment()
        {
            string[] depts = { "Engineering", "Cloud Computing", "Business Admin", "Architecture" };
            return depts[random.Next(depts.Length)];
        }

        public override void Info()
        {
            Console.WriteLine($"Name: {FullName} | Age: {Age} | Faculty: {Department}");
        }
    }

    class Graduate : Student
    {
        public string DegreeType { get; set; }
        public DateTime GraduationDate { get; set; }

        public Graduate(string name, string id, string dept, string degree) : base(name, id, dept)
        {
            DegreeType = degree;
            GraduationDate = GenerateRandomGraduationDate();
        }

        public Graduate() : base()
        {
            DegreeType = random.Next(2) == 0 ? "Master" : "PhD";
            GraduationDate = GenerateRandomGraduationDate();
        }

        private DateTime GenerateRandomGraduationDate()
        {
            // Fixed graduation date: June 15 (all students graduate on the same day each year)
            // Year varies between 2026-2030
            int graduationYear = random.Next(2026, 2031);
            return new DateTime(graduationYear, 6, 15);
        }

        public override void Info()
        {
            string graduationStatus = GraduationDate > DateTime.Now ? "Expected Graduation" : "Graduated";
            Console.WriteLine($"Name: {FullName} | Age: {Age} | Faculty: {Department} | Degree: {DegreeType} | {graduationStatus}: {GraduationDate:dd.MM.yyyy}");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            List<Student> studentList = new List<Student>();

            string[] namePool = {
                "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis",
                "David Wilson", "Jessica Taylor", "James Anderson", "Laura Martinez",
                "Daniel Thomas", "Olivia Harris", "Matthew Clark", "Sophia Lewis"
            };

            // Setup the initial admin/graduate student node
            Graduate initialGraduate = new Graduate();
            initialGraduate.FullName = namePool[0];
            initialGraduate.StudentId = "k00000";
            initialGraduate.Department = "Computer Science";
            initialGraduate.Score = 15;

            int maxStudentsCount = 10;
            List<string> idPool = new List<string>();

            initialGraduate.CreateIdPool(idPool, maxStudentsCount - 1);
            studentList.Add(initialGraduate);

            // Populate the list with random graduate students from the pool
            for (int i = 1; i < maxStudentsCount; i++)
            {
                Graduate tempGraduate = new Graduate();
                tempGraduate.FullName = namePool[i % namePool.Length];
                studentList.Add(tempGraduate);
            }

            // Distribute unique IDs from the pool
            for (int i = 1; i < studentList.Count; i++)
            {
                int lastIdx = idPool.Count - 1;
                string pickedValue = idPool[lastIdx];
                studentList[i].StudentId = "k00" + pickedValue;
                idPool.RemoveAt(lastIdx);
            }

            // Console Output Summary
            Console.WriteLine("--- School System Status ---");
            foreach (var s in studentList)
            {
                Console.WriteLine($"Name: {s.FullName,-15} | Age: {s.Age,-3} | ID: {s.StudentId} | Dept: {s.Department,-18} | Score: {s.Score}");
            }
            Console.WriteLine($"\nTotal Registered Students: {Student.GetStudentCount()}");

            Console.WriteLine("\n--- Info() Method Output ---");
            foreach (var s in studentList)
            {
                s.Info();
            }

            Console.WriteLine("\n======================================================\n");

            // LINQ Queries File Generation
            string filePath = "StudentReport.txt";

            using (StreamWriter writer = new StreamWriter(filePath))
            {
                // Write student system status
                writer.WriteLine("--- SCHOOL SYSTEM STATUS ---");
                writer.WriteLine($"Date Generated: {DateTime.Now}\n");
                writer.WriteLine("All Registered Students:");
                writer.WriteLine("----------------------------------------");
                foreach (var s in studentList)
                {
                    writer.WriteLine($"Name: {s.FullName,-15} | Age: {s.Age,-3} | ID: {s.StudentId} | Dept: {s.Department,-18} | Score: {s.Score}");
                }
                writer.WriteLine($"\nTotal Registered Students: {Student.GetStudentCount()}");
                writer.WriteLine("\n======================================================\n");

                // Write Info() method output for each student
                writer.WriteLine("--- DETAILED STUDENT INFORMATION ---\n");
                foreach (var s in studentList)
                {
                    if (s is Graduate grad)
                    {
                        string graduationStatus = grad.GraduationDate > DateTime.Now ? "Expected Graduation" : "Graduated";
                        writer.WriteLine($"[GRADUATE] Name: {grad.FullName} | Age: {grad.Age} | Faculty: {grad.Department} | Degree: {grad.DegreeType} | {graduationStatus}: {grad.GraduationDate:dd.MM.yyyy}");
                    }
                    else
                    {
                        writer.WriteLine($"[STUDENT] Name: {s.FullName} | Age: {s.Age} | Faculty: {s.Department}");
                    }
                }
                writer.WriteLine("\n======================================================\n");

                // LINQ Queries Report
                writer.WriteLine("--- LINQ QUERIES REPORT ---\n");

                // Query 1: Unenrolled candidates (Score < 10)
                writer.WriteLine("Candidates that cannot be enrolled (Score < 10):");
                var failedStudents = studentList.Where(s => s.Score < 10);
                foreach (var s in failedStudents)
                {
                    writer.WriteLine($"{s.FullName} - {s.Score} - {s.Department}");
                }
                writer.WriteLine("----------------------------------------");

                // Query 2: Engineering candidates with proper score
                writer.WriteLine("Candidates enrolled in Engineering (Score >= 10):");
                var engineeringStudents = studentList.Where(s => s.Department == "Engineering" && s.Score >= 10);
                foreach (var s in engineeringStudents)
                {
                    writer.WriteLine($"{s.FullName} - {s.Score} - {s.Department}");
                }
                writer.WriteLine("----------------------------------------");

                // Query 3: General Average Score
                double totalAverage = studentList.Average(s => s.Score);
                writer.WriteLine($"Average score for all candidates: {totalAverage:F2}");
                writer.WriteLine("----------------------------------------");

                // Query 4: Ordered by descending score (highest first)
                writer.WriteLine("Candidates by departments (Highest score first):");
                var orderedStudents = studentList.OrderByDescending(s => s.Score).ThenBy(s => s.Department);
                foreach (var s in orderedStudents)
                {
                    writer.WriteLine($"{s.FullName,-15} {s.Score,-4} Department: {s.Department}");
                }
                writer.WriteLine("----------------------------------------");

                // Query 5: Average score broken down by department
                writer.WriteLine("Average scores for all departments:");
                var averageByDept = studentList
                    .GroupBy(s => s.Department)
                    .Select(g => new
                    {
                        DeptName = g.Key,
                        AverageScore = g.Average(s => s.Score)
                    });

                foreach (var group in averageByDept)
                {
                    writer.WriteLine($"{group.DeptName,-18} {group.AverageScore:F2}");
                }
            }

            Console.WriteLine($"SUCCESS: LINQ report has been written to '{filePath}'!");

            // Student Search Interaction
            Console.Write("\nPlease enter the student number you wish to view (e.g. k00xxx): ");
            string searchId = Console.ReadLine();

            Student foundStudent = studentList.FirstOrDefault(s => s.StudentId == searchId);

            if (foundStudent != null)
            {
                Console.WriteLine("\n--- Student Information ---");
                foundStudent.Info();
                
                // Show additional graduation information if available
                if (foundStudent is Graduate grad)
                {
                    string graduationStatus = grad.GraduationDate > DateTime.Now ? "Expected to graduate on" : "Graduated on";
                    Console.WriteLine($"Status: {graduationStatus} {grad.GraduationDate:dd.MM.yyyy}");
                }
                else
                {
                    Console.WriteLine("Status: Currently Studying (Not yet graduated)");
                }
            }
            else
            {
                Console.WriteLine("No student found with that student number.");
            }
        }
    }
}