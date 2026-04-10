def zlicz_znaki(tekst): 
    slownik = {}
    for znak in tekst: 
        if znak in slownik: 
            slownik[znak] += 1
        else: 
            slownik[znak] = 1
    return slownik 

tekst_uzytkownika = input("Podaj tekst do analizy")
print(zlicz_znaki(tekst_uzytkownika))