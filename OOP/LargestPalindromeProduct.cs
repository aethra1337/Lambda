using System;

class PrimeFactors {
    
    static bool poli(int num)
    {
        string textNum = num.ToString();
        bool is_poli = true;
        for (int i = 0; i < textNum.Length / 2; i++)
            if (textNum[i] != textNum[textNum.Length - 1 - i])
            {
                is_poli = false;
                break;
            }    
        return is_poli;
    }

    static void Main() {
        int max = 0; // keep the largest result


        for (int i = 900; i < 999; i++)
        {
            for (int j = 900; j < 999; j++)
            {
                int product = i * j;

              
                if (poli(product))
                {
                
                    if (product > max)
                    {
                        max = product;
                    }
                }
            }
        }
        
        // Print the final result
        Console.WriteLine("Largest Palindrome: " + max);
    }
}