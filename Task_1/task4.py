def zamiana_temperatur():
    print("Dostępne konwersje:")
    print("C - z Celsjusza na Fahrenheita")
    print("F - z Farenheita na Celcjusza")
    
    typ = input("Wybierz typ konwersji (C/F): ").strip().upper()
    
    if typ not in ['C', 'F']: 
        print("Bledny wybór")
        return 
    
    wartosc = float(input("Podaj wartość temperatury: "))
    
    if typ == "C": 
        wynik = (wartosc * 9/5) + 32
        print(f"{wartosc}C to {wynik:.2f}F")
    else: 
        wynik = (wartosc - 32) * 5/9
        print(f"{wartosc}F to {wynik:.2}C")

zamiana_temperatur()
