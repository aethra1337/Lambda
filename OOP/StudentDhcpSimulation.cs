using System;
using System.Collections.Generic;

namespace SchoolSystemApp
{
    class Student
    {
        private string fullName;
        private string studentIp;
        private string department;
        private static int totalStudents = 0;

        public Student(string name, string ip, string dept)
        {
            fullName = name;
            studentIp = ip;
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

        public string StudentIp 
        { 
            get { return studentIp; } 
            set { studentIp = value; } 
        }

        public string Department 
        { 
            get { return department; } 
            set { department = value; } 
        }

        public static string GenerateId()
        {
            Random random = new Random();
            return random.Next(100, 999).ToString();
        }

        public void CreateIpPool(List<string> pool, int size)
        {
            while (pool.Count < size)
            {
                string newId = GenerateId();
                if (!pool.Contains(newId))
                {
                    pool.Add(newId);
                }
            }
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

            Student serverNode = new Student();
            serverNode.FullName = "Main_DHCP";
            serverNode.StudentIp = "10.0.0.1";
            serverNode.Department = "Engineering";

            int maxDevices = 6;
            List<string> ipPool = new List<string>();
            
            serverNode.CreateIpPool(ipPool, maxDevices - 1);
            studentList.Add(serverNode);

            for (int k = 1; k < maxDevices; k++)
            {
                Student temp = new Student("User_" + k, "", "Engineering");
                studentList.Add(temp);
            }

            for (int m = 1; m < studentList.Count; m++)
            {
                int lastIdx = ipPool.Count - 1;
                string pickedValue = ipPool[lastIdx];
                
                studentList[m].StudentIp = "10.0.0." + pickedValue;
                ipPool.RemoveAt(lastIdx);
            }

            Console.WriteLine("--- Network Status ---");
            foreach (var s in studentList)
            {
                Console.WriteLine("Name: " + s.FullName + " | IP: " + s.StudentIp);
            }

            Console.WriteLine("\nTotal Registered: " + Student.GetStudentCount());
        }
    }
}