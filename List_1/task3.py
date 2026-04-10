def odwracanie_ciagu(tekst): 
    odwrocony = ""
    for znak in tekst: 
        odwrocony = znak + odwrocony 
    return odwrocony 

print(odwracanie_ciagu("python"))