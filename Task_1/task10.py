def analiza(nazwa_pliku): 
    try: 
        with open(nazwa_pliku, "r", encoding="utf-8") as plik: 
            linie = plik.readlines() 
            
            liczba_linii = len(linie) 
            liczba_slow = sum(len(linia.split()) for linia in linie) 
            liczba_znakow = sum(len(linia) for linia in linie)
            
            print(f"statysyki dla pliku '{nazwa_pliku}':")
            print(f"liczba linii: {liczba_linii}")
            print(f"liczba slow: {liczba_slow}")
            print(f"liczba znakow: {liczba_znakow}")
    except: 
        print(f"Blad: Plik '{nazwa_pliku}' nie zostal znaleziony")
        
analiza("dane.txt")