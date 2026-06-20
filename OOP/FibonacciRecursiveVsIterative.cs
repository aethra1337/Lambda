using System;

class FiboNumbers {
    
    static long fibo(int n)
    {
        if (n == 1 || n == 2) return n;
            else
        return fibo(n-1) + fibo(n-2);
    }
    
    static long fibo2(int n)
    {   
        int result=0;
        int a = 1;
        int b = 2;
        int temp;
        for (int i=3; i<=n; i++)
        {
            result=a+b;
            temp=a;
            b=a;
            a=result;
        }
        return result;
    }
    
    
    
    
    
  static void Main() {
    for(int i = 1; i<10; i++) 
    Console.WriteLine("{0} {1} {2}", i, fibo(i), fibo2(i));
    
    
  }
}