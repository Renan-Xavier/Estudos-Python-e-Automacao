votos_segunda = 0
votos_terca = 0
votos_quarta = 0
votos_quinta = 0
votos_sexta = 0

n = int(input("Informe o número de colaboradores "))

for i in range(n):
    dia = input("Informe o dia da sua preferência (segunda-feira, terça-feira, quarta-feira, quinta-feira, sexta-feira): ")
    if dia == "segunda-feira":
        votos_segunda += 1
    elif dia == "terça-feira":
        votos_terca += 1
    elif dia == "quarta-feira":
        votos_quarta += 1
    elif dia == "quinta-feira":
        votos_quinta += 1
    elif dia == "sexta-feira":
        votos_sexta += 1

maior = votos_segunda
if votos_terca > maior:
    maior = votos_terca
if votos_quarta > maior:
    maior = votos_quarta
if votos_quinta > maior:
    maior = votos_quinta
if votos_sexta > maior:
    maior = votos_sexta

vencedores = []
if votos_segunda == maior:
    vencedores.append("segunda-feira")
if votos_terca == maior:
    vencedores.append("terça-feira")
if votos_quarta == maior:
    vencedores.append("quarta-feira")
if votos_quinta == maior:
    vencedores.append("quinta-feira")
if votos_sexta == maior:
    vencedores.append("sexta-feira")

if len(vencedores) == 1:
    print("\nDia escolhido pelos colaboradores é:", vencedores[0], f"({maior} votos)")
else:
    print("\nEmpate entre:")
    for d in vencedores:
        print("-", d)
    print(f"com {maior} votos cada")