using System;

namespace OOP_in_Csharp
{
    class Student
    {
        // Private fields (Encapsulation)
        private string _name;
        private int _age;
        public string Faculty; // Public field as in your example

        // Static member to count total students
        private static int _counter = 0;

        // Constructor with parameters
        public Student(string name, int age, string faculty)
        {
            _name = name;
            _age = age;
            Faculty = faculty;
            _counter++; // Increase count for each new student
        }

        // Empty constructor (Default)
        public Student()
        {
            _counter++;
        }

        // Static method to access the private counter
        public static int GetStudentCount()
        {
            return _counter;
        }

        // Properties (Getter and Setter)
        public string Name
        {
            get { return _name; }
            set { _name = value; }
        }

        public int Age
        {
            get { return _age; }
            set { _age = value; }
        }
    }

    class Program
    {
        static Random random = new Random();

        // Helper to get random age between 19-26
        static int GetRandomAge()
        {
            return random.Next(19, 27);
        }

        // Helper to get a random faculty
        static string GetRandomFaculty()
        {
            string[] faculties = { "Engineering", "Medicine", "Law", "Arts" };
            return faculties[random.Next(faculties.Length)];
        }

        public static void Main(string[] args)
        {
            Student[] students = new Student[5];

            Student headStudent = new Student();
            headStudent.Name = "Rector";
            headStudent.Age = 40;
            headStudent.Faculty = "Administration";
            students[0] = headStudent;

            // 2. Filling the rest with random data
            for (int i = 1; i < students.Length; i++)
            {
                students[i] = new Student(
                    "Student" + i,
                    GetRandomAge(),
                    GetRandomFaculty()
                );
            }

            // 3. Printing the list
            Console.WriteLine("{0,-15} {1,-5} {2,-15}", "Name", "Age", "Faculty");
            Console.WriteLine("------------------------------------------");
            for (int i = 0; i < students.Length; i++)
            {
                Console.WriteLine("{0,-15} {1,-5} {2,-15}", 
                    students[i].Name, students[i].Age, students[i].Faculty);
            }

            // 4. Using the static method
            Console.WriteLine("\nTotal Students registered: {0}", Student.GetStudentCount());
        }
    }
}