import json
import socket
import select
import sys
import threading

# define a localizacao do servidor
HOST = ''  # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10001  # porta de acesso

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
# armazena historico de conexoes
conexoes = {}


def acessa_dados():
    with open("dicionario.json", "r") as infile:
        json = infile.read()
        dicionario = json.loads(json)
        return dicionario


def carrega_dados(dicionario):
    with open("dicionario.json", "r") as outfile:
        json = json.dumps(dicionario)


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

    return sock


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
        data = processa_requisicao(str(data, encoding='utf-8'), str(endr))
        clisock.send(data)  # ecoa os dados para o cliente


def processa_requisicao(requisicao, endr):
    if requisicao[0] == "p":
        print(f"{endr}: inserindo {requisicao}")
        return resp
    elif requisicao[0] == "g":
        print(f"{endr}: consultando {requisicao}")
        return resp
    else:
        print("requisição falha")
    return


def main():
    '''Inicializa e implementa o loop principal (infinito) do servidor'''
    clientes = []  # armazena as threads criadas para fazer join
    sock = iniciaServidor()
    print("Pronto para receber conexoes...")
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
                cmd = input("teste")
                if cmd == 'fim':  # solicitacao de finalizacao do servidor
                    for c in clientes:  # aguarda todas as threads terminarem
                        c.join()
                    sock.close()
                    sys.exit()
                elif cmd == 'hist':  # outro exemplo de comando para o servidor
                    print(str(conexoes.values()))


if __name__ == '__main__':
    main()
