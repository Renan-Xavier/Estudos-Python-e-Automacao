a = int(input(" digite um valor inteiro: "))
lista = []

for x in range(a):
  b = input( 'digite letra ou numero: ')
  lista.append(b)
j = int(input("digite o primeiro numero de indice: "))
i = int(input("digite o segundo numero de indice: "))

temp = lista[j]
lista[j] = lista[i]
lista[i] = temp
print(lista)