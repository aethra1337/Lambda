using System; 

class ForLoop {
    static void Main()
    {
        // Doğru yazım: Başlangıç; Koşul; Artış miktarı
        for (int i = 0; i <= 100; i += 5) 
        {
            Console.WriteLine(i);
        }
        
        Console.ReadKey();
    }
}