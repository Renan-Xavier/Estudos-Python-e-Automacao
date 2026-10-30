print("Escolha o tipo de investimento:")
print("1. CDB")
print("2. LCI")
print("3. LCA")

tipo = input("Digite o tipo de investimento (1, 2 ou 3): ")

while tipo != "1" and tipo != "2" and tipo != "3":
	tipo = input("Digite o tipo de investimento (1, 2 ou 3): ")

valor_resgate = float(input("Digite o valor a ser resgatado: "))

while valor_resgate <= 0:
	valor_resgate = float(input("Digite o valor a ser resgatado: "))

dias = int(input("Digite o número de dias que o valor permaneceu investido: "))

while dias <= 0:
	dias = int(input("Digite o número de dias que o valor permaneceu investido: "))

imposto = 0.0

if tipo == "1":  
	if dias <= 180:
		imposto = valor_resgate * 0.225
	elif dias <= 360:
		imposto = valor_resgate * 0.20
	elif dias <= 720:
		imposto = valor_resgate * 0.175
	else:
		imposto = valor_resgate * 0.15
else:
	imposto = 0.0  

print("O valor do imposto de renda a ser pago é: R$ " + "{:.2f}".format(imposto))

