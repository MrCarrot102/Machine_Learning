def silnia(n): 
    if (n <= 1):
        return 1 
    
    return n * silnia(n - 1)

print (f"Silnia z 5 to: {silnia(5)}")