divida = float(input("Digite o valor da dívida:"))

while divida <= 0:
	divida = float(input("Digite o valor da dívida:"))

quantidade = 1
percentual = 0

while True:
	valor_juros = divida * percentual / 100
	total = divida + valor_juros
	valor_parcela = total / quantidade

	total_str = ("{:.2f}".format(total)).replace(".", ",")
	juros_str = ("{:.2f}".format(valor_juros)).replace(".", ",")
	parcela_str = ("{:.2f}".format(valor_parcela)).replace(".", ",")

	print(
		"Total:R$ "
		+ total_str
		+ " Juros:R$ "
		+ juros_str
		+ " Número de parcelas:"
		+ str(quantidade)
		+ " Valor da Parcela:R$ "
		+ parcela_str
	)

	if quantidade == 1:
		quantidade = 3
		percentual = 10
	elif quantidade == 3:
		quantidade = 6
		percentual = 15
	elif quantidade == 6:
		quantidade = 9
		percentual = 20
	elif quantidade == 9:
		quantidade = 12
		percentual = 25
	else:
		break


