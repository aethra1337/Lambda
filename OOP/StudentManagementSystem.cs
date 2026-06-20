using System;
using System.Collections.Generic;

namespace OOP_in_Csharp
{
    class Student
    {
        // Alanlar (Fields) - Private oldukları için küçük harf ve alt çizgi standarttır.
        private string _name;
        private int _age;
        private string _faculty;
        private static int _counter = 0;

        // Statik Random: Her metot çağrıldığında yeni nesne oluşup aynı sayıyı üretmesin diye tek bir tane tanımlanır.
        private static Random _random = new Random();

        // Yapıcı Metotlar (Constructors)
        public Student(string name, int age, string faculty)
        {
            this._name = name;
            this._age = age;
            this._faculty = faculty;
            _counter++;
        }

        public Student()
        {
            _counter++;
        }

        public static int GetStudNum()
        {
            return _counter;
        }

        // Özellikler (Properties) - Public oldukları için büyük harfle başlarlar.
        public string Name
        {
            get { return this._name; }
            set { this._name = value; }
        }

        public int Age
        {
            get { return this._age; }
            set { this._age = value; }
        }

        public string Faculty
        {
            get { return this._faculty; }
            set { this._faculty = value; }
        }

        // Yardımcı Metotlar
        public static int GetRandomAge()
        {
            return _random.Next(19, 27);
        }

        public static string GetRandomFaculty()
        {
            string[] faculties = { "Engineering", "Medicine", "Law", "Arts", "Business" };
            return faculties[_random.Next(faculties.Length)];
        }

        public void StartStudy()
        {
            this.Age = GetRandomAge();
            this.Faculty = GetRandomFaculty();
        }
    }

    class Program
    {
        // Dersi bitirenleri/bırakanları yöneten metot
        static void FinishStudy(List<Student> students, string studName)
        {
            for (int i = 0; i < students.Count; i++)
            {
                if (students[i].Name == studName)
                {
                    // Silmeden hemen önce ekrana yazdırarak hocanın istediği bildirimi yapıyoruz.
                    Console.WriteLine("--> INFO: {0} has finished/dropped the study.", students[i].Name);
                    students.RemoveAt(i);
                    i--; // Liste daraldığı için bir sonraki elemanı atlamamak için indeksi geri çekiyoruz.
                }
            }
        }

        private static void Main(string[] args)
        {
            List<Student> studentList = new List<Student>();

            // 1. Rektör Nesnesi Oluşturma
            Student rector = new Student();
            rector.Name = "RECTOR";
            rector.Age = 40;
            rector.Faculty = "Admin";
            studentList.Add(rector);

            // 2. Diğer Öğrencileri Başlangıç Değerleriyle Ekleme
            const int totalCapacity = 5;
            for (int i = 1; i < totalCapacity; i++)
            {
                studentList.Add(new Student("stud" + i, 0, "Pending..."));
            }

            // 3. Çalışma Başlatma ve Listeleme
            Console.WriteLine("{0,-15} {1,-5} {2,-15}", "Name", "Age", "Faculty");
            Console.WriteLine(new string('-', 40));

            for (int i = 0; i < studentList.Count; i++)
            {
                studentList[i].StartStudy();
                Console.WriteLine("{0,-15} {1,-5} {2,-15}", studentList[i].Name, studentList[i].Age, studentList[i].Faculty);
            }

            // 4. Ayrılan Öğrencilerin İşlenmesi
            Console.WriteLine("\n--- Processing Departures ---");
            FinishStudy(studentList, "stud1");
            FinishStudy(studentList, "stud3");

            // 5. Kalan Öğrenci Listesinin Gösterilmesi
            Console.WriteLine("\n--- Remaining Students List ---");
            foreach (Student s in studentList)
            {
                Console.WriteLine("{0,-15} {1,-5} {2,-15}", s.Name, s.Age, s.Faculty);
            }

            // 6. Toplam Üretilen Nesne Sayısı (Static Counter)
            Console.WriteLine("\nTotal student objects created in history: {0}", Student.GetStudNum());
            
            Console.WriteLine("\nPress Enter to exit...");
            Console.ReadLine();
        }
    }
}