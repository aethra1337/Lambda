using System;

namespace OOP_in_Csharp
{
    public class Student 
    {
        public string Name;    
        public int Age;       
        public string Faculty; 

        public Student(string name, int age, string faculty)
        {
            Name = name;
            Age = age;
            Faculty = faculty;
        }
    }

    class Program
    {
        static Random random = new Random();

        static int GetRandomAge()
        {
            return random.Next(19, 25);
        }


        static string GetRandomFaculty()
        {
            string[] faculties = { "Engineering", "Medicine", "Law", "Arts", "Business" };
            int index = random.Next(faculties.Length);
            return faculties[index];
        }

        public static void Main(string[] args)
        {
            Student[] students = new Student[6]; 

            for (int i = 0; i < students.Length; i++)
            {
                students[i] = new Student(
                    "Student" + (i + 1), 
                    GetRandomAge(), 
                    GetRandomFaculty() 
                );
            }

            Console.WriteLine("{0,-15} {1,-5} {2,-15}", "Name", "Age", "Faculty");
            Console.WriteLine("                                                ");
            
            foreach (var student in students)
            {
               
                Console.WriteLine("{0,-15} {1,-5} {2,-15}", 
                    student.Name, student.Age, student.Faculty);
            }
        }
    }
}