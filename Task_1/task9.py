def tabliczka_mnozenia(): 
    for i in range(1, 11):
        for j in range(1, 11): 
            print(f"{i * j:4}", end="")
        print()
        
tabliczka_mnozenia()