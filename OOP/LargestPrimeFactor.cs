using System;

public class Program
{
    public static void Main()
    {
        
        long number = 600851475143; 
        long divisor = 2;
        
        while (divisor * divisor <= number)
        {
            if (number % divisor == 0)
            {
                // this part removes the current prime factor from the number
                number /= divisor;
            }
            else
            {
                // If that number is not divisible then increment to the next possible divisor
                divisor++;
            }
        }


        Console.WriteLine("Largest prime factor: " + number);
    }
}