preco = float(input("Digite o preço do carro:"))

while preco <= 0:
	preco = float(input("Digite o preço do carro:"))

desconto = preco * 0.20
preco_avista = preco - desconto

print("O preço final á vista com desconto 20% é:" + str(preco_avista))

parcelas = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
acrescimos = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]

indice = 0
while indice < len(parcelas):
	quantidade = parcelas[indice]
	percentual = acrescimos[indice]
	acrescimo = preco * percentual / 100
	preco_final = preco + acrescimo
	valor_parcela = preco_final / quantidade

	preco_final_str = ("{:.2f}".format(preco_final)).replace(".", ",")
	parcela_str = ("{:.2f}".format(valor_parcela)).replace(".", ",")

	print("O preço final parcelado em " + str(quantidade) + " X é de R$ " + preco_final_str + " com parcelas de R$ " + parcela_str)

	indice = indice + 1

