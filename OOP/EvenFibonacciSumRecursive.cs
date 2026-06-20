using System;
class FiboNumbers {
    
    static int fibo(int n)
    {
        if (n == 1 || n == 2) return n;
            else
        return fibo(n-1) + fibo(n-2);
        
    }
    
  static void Main() {
    int i = 1;
    int term = 0;
    int total = 0;
    while(term < 4000000)
    {
        term = fibo(i);
        if(term %2 == 0)
        {
            total += term;
        }
        i++;
    }
    Console.WriteLine(total);
  }
}