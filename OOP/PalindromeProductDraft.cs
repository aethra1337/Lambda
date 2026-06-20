using System;

public class Program
{
    public static void Main()
    {
        int largest = 0; // "largest" dedik ama her şeyi ekrana basıyoruz

        for (int i = 900; i <= 999; i++)
        {
            for (int j = 900; j <= 999; j++)
            {
                int res = i * j;
                
                // Gereksiz yere string'e çevirip bir de fonksiyona yolluyoruz
                string s = res.ToString(); 

                if (isPal(s)) // Fonksiyon ismini tam yazmadık (isPal)
                {
                    Console.WriteLine(i + " çarpı " + j + " eşittir " + res);
                    largest = res; 
                }
            }
        }
        // En son sadece en büyük olanı değil, döngüdeki son sonucu yazar
        Console.WriteLine("Son bulunan: " + largest); 
    }

    static bool isPal(string text)
    {
        string rev = "";
        // k++ yerine k-- yaparken kafası karışmış gibi
        for (int k = text.Length - 1; k >= 0; k--)
        {
            rev = rev + text[k];
        }

        // Gereksiz if-else kullanımı (yeni başlayanlar genelde böyle yapar)
        if (text == rev)
        {
            return true;
        }
        else
        {
            return false;
        }
    }
}




using System;
class PrimeFactors {
    
    static bool poli(int num)
    {
    string textNum = num.ToString();
    bool is_poli = true;
    for (int i=0; i<textNum.Length/2;i++)
        if (textNum[i] != textNum[textNum.Length-1-i])
        {
            is_poli = false;
            break;
        }    
    return is_poli;
    }

      static void Main() {
       
       for(int i =1; i<100;i++)
       {
           if(poli(i))
           {
           Console.WriteLine(i +"   "+ poli(i));               
           }
       }
       
     }
    
}

//