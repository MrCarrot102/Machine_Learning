def czy_pierwsza(n): 
    if (n <= 1):
        return False
    
    for i in range(2, int(n**0.5 + 1)): 
        if (n % i == 0):
            return False 
    
    return True
    
for i in range (0, 100): 
    print (f"{i} czy jest liczbą pierwszą: {czy_pierwsza(i)}")
