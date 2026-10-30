# Lista direta loop direta sem indice

notas = []

for x in range(5):
    codigo_aluno = input("RM: ")
    nota = float(input("Nota: "))
    resultado = [codigo_aluno, nota]
    notas.append(resultado)

for n in notas:
    codigo_aluno = n[0]
    nota = n[1]
    print("O RM:", codigo_aluno,"tirou nota:", nota)