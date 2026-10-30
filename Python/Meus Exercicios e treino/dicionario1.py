import os

mensagens = [] # armazena as mensagens

nome = input("nome: ")

while True: # Loop infinito

    os.system('cls') # limpa o terminal/tela

    if len(mensagens) > 0: # verifica quantida de mensagens(só irá ativar o FOR se tiver pelo menos 1 item/mensagem na lista)
        for m in mensagens: # percorre a lista de mensagens
            print(m['nome'], "-", m['texto'])   # exibe o nome do usario que está enviando a mensagem recebida pela valiavel nome input.

    print("________________________________")

    # obtenção do texto da mensagem

    texto = input("mensagem: ")
    if texto == "fim":
        break

    # adcionando mensagem na lista 

    mensagens.append({  # adiciona um dicionario com nome e texto na lista mensagens
        'nome': nome, 
        'texto': texto
        })
 