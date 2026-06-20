using System;

class Program
{
    static void Main()
    {
        int limit = 4000000;
        int sum = 0;
        int a = 1;
        int b = 2;

        while (b <= limit)
        {
            // Add the even numbers
            if (b % 2 == 0)
            {
                sum += b;
            }

            // Calculate nex fibo number
            int next = a + b;
            a = b;
            b = next;
        }

        Console.WriteLine("Result: " + sum);
    }
}
