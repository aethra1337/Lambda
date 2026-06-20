using System;

class FindingPi {
    // Euler'in Basel Problemi: 1/1^2 + 1/2^2 + 1/3^2 ... 
    static double euler(int rep)
    {
        double total = 0;

        for (int i = 1; i < rep; i++)
        {
            // i*i ile kareyi alıyoruz, 1.0 ile bölerek ondalıklı sonuç alıyoruz
            double term = 1.0 / ((double)i * i);
            total += term;
        }

        return total; // Bu değer pi^2 / 6'ya yaklaşır
    }

    static void Main() {
        // Karşılaştırma yapacağımız hedef değer: (pi * pi) / 6
        double pi = 3.141592653589793238;
        double hedef = (pi * pi) / 6; 
        
        double sonucumuz = euler(10000); 

        Console.WriteLine("Seri Toplamı: {0}", sonucumuz);
        Console.WriteLine("Hedef (pi^2/6): {0}", hedef);
        Console.WriteLine("Fark: {0}", hedef - sonucumuz);
    }
}