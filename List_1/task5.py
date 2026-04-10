def usun_duplikaty(lista):
    return list(set(lista))

def usun_duplikaty(lista): 
    nowa_lista = []
    for element in lista: 
        if element not in nowa_lista: 
            nowa_lista.append(element)
    return nowa_lista 

print(usun_duplikaty([1,2,2,3,4,4,5]))