using System;

class Program
{
    static void Main()
    {
        // Kullanıcıdan giriş alma
        Console.Write("Santimetre (cm) değerini giriniz: ");
        double cm = Convert.ToDouble(Console.ReadLine());

        // Dönüşüm hesabı (1 inç = 2.54 cm)
        double inch = cm / 2.54;

        // Sonucu ekrana yazdırma (Virgülden sonra 2 basamak)
        Console.WriteLine($"{cm} cm = {inch:F2} inç eder.");
        
        // Programın hemen kapanmaması için
        Console.ReadLine();
    }
}