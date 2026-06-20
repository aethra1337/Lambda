using System;
using System.Collections.Generic;

namespace SchoolSystemApp
{
    class Student
    {
        private string fullName;
        private string studentId; 
        private string department;
        private static int totalStudents = 0;

        public Student(string name, string id, string dept)
        {
            fullName = name;
            studentId = id;
            department = dept;
            totalStudents++;
        }

        public Student()
        {
            totalStudents++;
        }

        public static int GetStudentCount()
        {
            return totalStudents;
        }

        public string FullName 
        { 
            get { return fullName; } 
            set { fullName = value; } 
        }

        public string StudentId 
        { 
            get { return studentId; } 
            set { studentId = value; } 
        }

        public string Department 
        { 
            get { return department; } 
            set { department = value; } 
        }

        public static string GenerateIdSuffix()
        {
            Random random = new Random();
            return random.Next(100, 999).ToString();
        }

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
    }

    // --- GRADUATE (MEZUN) SINIFI ---
    class Graduate : Student
    {
        private string degreeType; 

        public Graduate(string name, string id, string dept, string degree) : base(name, id, dept)
        {
            this.degreeType = degree;
        }

        public Graduate() : base()
        {
            this.degreeType = GetRandomDegree();
        }

        public string DegreeType
        {
            get { return degreeType; }
            set { degreeType = value; }
        }

        private string GetRandomDegree()
        {
            string[] degrees = { "Master", "PhD" };
            Random rnd = new Random();
            int index = rnd.Next(degrees.Length); 
            return degrees[index];
        }
    }

    class Program
    {
        static void RemoveStudent(List<Student> list, string targetName)
        {
            for (int i = 0; i < list.Count; i++)
            {
                if (list[i].FullName == targetName)
                {
                    list.RemoveAt(i);
                    break; 
                }
            }
        }

        public static void Main(string[] args)
        {
            List<Student> studentList = new List<Student>();

            Graduate serverNode = new Graduate();
            serverNode.FullName = "Graduate_Admin_DHCP";
            serverNode.StudentId = "k00000"; 
            serverNode.Department = "Computer Science";

            int maxDevices = 6;
            List<string> idPool = new List<string>(); 
            
            serverNode.CreateIdPool(idPool, maxDevices - 1);
            studentList.Add(serverNode); 

            for (int k = 1; k < maxDevices; k++)
            {
                Student temp = new Student("User_" + k, "", "Engineering");
                studentList.Add(temp);
            }

            for (int m = 1; m < studentList.Count; m++)
            {
                int lastIdx = idPool.Count - 1;
                string pickedValue = idPool[lastIdx];
                
                studentList[m].StudentId = "k00" + pickedValue;
                idPool.RemoveAt(lastIdx);
            }

            Console.WriteLine("--- School System Status ---");
            foreach (var s in studentList)
            {
                if (s is Graduate g)
                {
                    Console.WriteLine("Name: " + g.FullName + " [Graduate - " + g.DegreeType + "] | Student ID: " + g.StudentId);
                }
                else
                {
                    Console.WriteLine("Name: " + s.FullName + " | Student ID: " + s.StudentId);
                }
            }

            Console.WriteLine("\nTotal Registered (Students + Graduates): " + Student.GetStudentCount());
        }
    }
}