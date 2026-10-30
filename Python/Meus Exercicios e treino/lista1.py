# trocar valores de uma variavel em uma lista

lista = [10, 2, 5, 0, 6, 0]
for i in range(len(lista)):             # para percorrer toda a lista
    if lista[i] == 0 and lista[i] < 5:  # se o valor for igual a 0 e menor que 5
        lista[i] = 4                    # troca o valor 0 por 4
print(lista)

# para executar eu preciso digitar no terminal: python lista1.py  E verificar se o terminal está na pasta correta.