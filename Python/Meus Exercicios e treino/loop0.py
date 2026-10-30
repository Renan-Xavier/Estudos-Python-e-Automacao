# Loop para lista dentro de lista com representação de notas de alunos

notas = []

for x in range(5):                    # Loop para adicionar 5 notas
    codigo_aluno = input("RM: ")      # Solicita o RM do aluno
    nota = float(input("Nota: "))     # Solicita a nota do aluno
    resultado = [codigo_aluno, nota]  # Cria uma sublista com RM e nota
    notas.append(resultado)           # Adiciona a sublista à lista principal

for n in notas:
    codigo_aluno = n[0]                               # Acessa o RM do aluno
    nota = n[1]                                       # Acessa a nota do aluno
    print("O RM:", codigo_aluno,"tirou nota:", nota)  # Exibe o RM e a nota

# para executar eu preciso digitar no terminal: python loop0.py  E verificar se o terminal está na pasta correta.