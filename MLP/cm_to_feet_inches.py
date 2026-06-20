# Santimetreden Feet ve inç dönüştürücü
def simple_converter():
    print("Santimetreden Feet ve inç dönüştürücü")
    
    try:
        # Girdi alınız
        cm = float(input("CM giriniz: "))
        
        # 1 cm = 0.3937 inches
        total_inches = cm * 0.3937
        
        # 1 cm  0.0328 feet
        total_feet = cm * 0.0328
        
        # Sonuç Göster
        print(f"{cm} cm esittir {total_feet:.2f} feet")
        print(f"{cm} cm esittir {total_inches:.2f} inches")
        
    except ValueError:
        print("Lütfen numerik bir değer giriniz")

# Çalıştır
simple_converter()