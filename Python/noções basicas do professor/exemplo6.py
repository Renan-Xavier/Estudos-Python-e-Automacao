# solicitar as 3 notas de um aluno e a quantidade de faltas.
# Verificar se o aluno foi aprovado
# Aprovado se a média >= 6 e quantidade faltas <= 20

nota1 = float(input("Digite sua primeira nota: "))
nota2 = float(input("Digite sua segunda nota: "))
nota3 = float(input("Digite sua terceira nota: "))
faltas = int(input("Digite a quantidade de faltas: "))

media = (nota1 + nota2 + nota3) / 3
print(f"Média: {media}")

print(f"O aluno foi aprovado? {media >= 6 and faltas <= 20}")
