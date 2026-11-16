lista = [1,4,6,9,42,12,15,100,78,89,76,345,123,53,78,534,132,345,675,]
lista.sort()

inicio = 0
fim = len(lista)
buscas =0
num = int(input("qual numero deseja procurar: "))

print(lista)
while inicio <= fim:
    meio = (inicio + fim) //2
    print(meio)
    if lista[meio] == num:
        buscas+=1
        print(f"index: {meio}, buscas: {buscas}")
        break

    elif num > lista[meio]:
        buscas+=1
        inicio = meio + 1
        print(lista[inicio:fim])
            
    else:
        buscas+=1
        fim = meio - 1
        print(lista[inicio:fim])



