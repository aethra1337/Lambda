using System;

public class Program
{
    public static void Main()
    {
        int n = 10; 
        long ilkSayi = 1; 
        long ikinciSayi = 1;

        for (int i = 1; i <= n; i++) 
        {
            int basamakSayisi = ilkSayi.ToString().Length;

            
            Console.WriteLine($"{i}. term ({basamakSayisi} digit) :");
            Console.WriteLine(ilkSayi);
            Console.WriteLine(); 
            
            long sonrakiSayi = ilkSayi + ikinciSayi;
            ilkSayi = ikinciSayi;
            ikinciSayi = sonrakiSayi;
        }
    }
}