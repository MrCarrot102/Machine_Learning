import random 

def zgadywanie(): 
    szukana_liczba = random.randint(1, 20)
    print("zgadnij liczbe z zakresu od 1 do 20")
    
    while True: 
        try: 
            proba = int(input("Podaj liczbe: "))
            
            if (proba < szukana_liczba): 
                print("za mala")
            elif (proba > szukana_liczba): 
                print("za duza")
            else: 
                print("Brawo! Zgadles")
                break
        except ValueError: 
            print("to nie jest poprawna liczba calkowita")


zgadywanie()