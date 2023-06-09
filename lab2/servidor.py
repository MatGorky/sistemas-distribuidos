import json
import socket
import select
import sys
import threading

# define a localizacao do servidor
HOST = ''  # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10005  # porta de acesso

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
# armazena historico de conexoes
conexoes = {}


# função para carregar o arquivo do disco e escrever em um dicionário na memória
def acessa_dados():
    with open("dicionario.json", "r") as infile:
        if infile.read().strip() == '':
            dicionario = {}  # Se o arquivo estiver vazio
        else:
            # Senão, carregamos o json
            infile.seek(0)
            dicionario = json.load(infile)
        return dicionario

# função para receber o dicionário da memória e guardar o arquivo no disco


def guarda_dados(dicionario):
    with open("dicionario.json", "w") as outfile:
        json.dump(dicionario, outfile)


def iniciaServidor():
    '''Cria um socket de servidor e o coloca em modo de espera por conexoes
    Saida: o socket criado'''
    # cria o socket
    # Internet( IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # vincula a localizacao do servidor
    sock.bind((HOST, PORT))

    # coloca-se em modo de espera por conexoes
    sock.listen(5)

    # configura o socket para o modo nao-bloqueante
    sock.setblocking(False)

    # inclui o socket principal na lista de entradas de interesse
    entradas.append(sock)

    checa_arquivo()
    return sock

# Garante que o arquivo vai existir, pois se não existir, ele será criado


def checa_arquivo():
    try:
        # tenta abrir o arquivo em modo de escrita
        with open('dicionario.json', '+r') as arquivo:
            print("Arquivo existente")

    except FileNotFoundError:
        # se ocorrer um erro de arquivo não encontrado, cria o arquivo
        with open('dicionario.json', '+w') as arquivo:
            print("Arquivo criado com sucesso!")


def aceitaConexao(sock):
    '''Aceita o pedido de conexao de um cliente
    Entrada: o socket do servidor
    Saida: o novo socket da conexao e o endereco do cliente'''

    # estabelece conexao com o proximo cliente
    clisock, endr = sock.accept()

    # registra a nova conexao
    conexoes[clisock] = endr

    return clisock, endr


def atendeRequisicoes(clisock, endr):
    '''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
    Entrada: socket da conexao e endereco do cliente
    Saida: '''

    while True:
        # recebe dados do cliente
        data = clisock.recv(1024)
        if not data:  # dados vazios: cliente encerrou
            print(str(endr) + '-> encerrou')
            clisock.close()  # encerra a conexao com o cliente
            return
        else:
            data = processa_requisicao(str(data, encoding='utf-8'), str(endr))
            clisock.send(data.encode())  # envia a resposta para o cliente


# processa a requisião, se for um "post" é para inserir, se for um "get" para consultar
# neste sistema, outros tipos de requisição não são possíveis
def processa_requisicao(requisicao, endr):
    if requisicao[0] == "p":
        print(f"{endr}: inserindo {requisicao}")
        return registra(requisicao[1:])
    elif requisicao[0] == "g":
        print(f"{endr}: consultando {requisicao}")
        return consulta(requisicao[1:])
    else:
        print("requisição falha")
    return


def consulta(requisicao):
    dicionario = acessa_dados()
    if requisicao in dicionario:
        return f"O valor da chave consultada é: {dicionario[requisicao]}"
    else:
        return f"Chave não encontrada"


def registra(requisicao):
    # separando a chave do resto da string, que se tornará o valor
    requisicao = requisicao.split(maxsplit=1)

    string_resposta = ""
    chave = requisicao[0]
    if len(requisicao) > 1:  # if para o caso do valor ser vazio
        valor = requisicao[1]
    else:
        valor = ""

    # acessando os dados para saber se a chave será inserida ou rescrita
    dicionario = acessa_dados()
    if chave in dicionario:
        string_resposta = f"A chave '{chave}' já se encontrava no dicionário, valor reescrito"
    else:
        string_resposta = f"A chave '{chave}' não se encontrava no dicionário, valor inserido"
    dicionario[chave] = valor
    guarda_dados(dicionario)
    return string_resposta


def remove(chave):
    dicionario = acessa_dados()
    if chave in dicionario:
        del dicionario[chave]
        guarda_dados(dicionario)
        print(f"A chave '{chave}' foi removida com sucesso")
    else:
        print("Chave não encontrada")


def main():
    '''Inicializa e implementa o loop principal (infinito) do servidor'''
    clientes = []  # armazena as threads criadas para fazer join
    sock = iniciaServidor()
    print("Pronto para receber conexoes...")
    print("Digite fim se quiser fechar o servidor, digite 'remover <chave>', se quiser remover uma chave do dicionário")
    while True:
        # espera por qualquer entrada de interesse
        leitura, escrita, excecao = select.select(entradas, [], [])
        # tratar todas as entradas prontas
        for pronto in leitura:
            if pronto == sock:  # pedido novo de conexao
                clisock, endr = aceitaConexao(sock)
                print('Conectado com: ', endr)
                # cria nova thread para atender o cliente
                cliente = threading.Thread(
                    target=atendeRequisicoes, args=(clisock, endr))
                cliente.start()
                # armazena a referencia da thread para usar com join()
                clientes.append(cliente)
            elif pronto == sys.stdin:  # entrada padrao
                cmd = input()
                if cmd:
                    cmd = cmd.split(maxsplit=1)
                else:
                    continue
                if cmd[0] == 'fim':  # solicitacao de finalizacao do servidor
                    for c in clientes:  # aguarda todas as threads terminarem
                        c.join()
                    sock.close()
                    sys.exit()
                elif cmd[0] == 'remover':  # outro exemplo de comando para o servidor
                    if len(cmd) > 1:
                        remove(cmd[1])
                    else:
                        print("Não há chave vazia")


if __name__ == '__main__':
    main()
