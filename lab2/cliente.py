# servidor de echo: lado cliente
import socket
import os
import platform

HOST = 'localhost'  # maquina onde esta o servidor
PORT = 10005      # porta que o servidor esta escutando

clear = ""

# como é um sistema simples, irei utilizar números para definir a ação
# 0 é tela inicial, 1 é registro, 2 é consultar e 3 é finalizar o sistema
modo = 0


def iniciaCliente():
    '''Cria um socket de cliente e conecta-se ao servidor.
    Saida: socket criado'''
    # cria socket
    # Internet (IPv4 + TCP)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # conecta-se com o servidor
    sock.connect((HOST, PORT))

    # apenas definindo o comando para limpeza do console
    global clear
    if platform.system() == 'Windows':
        clear = 'cls'
    else:
        clear = 'clear'

    return sock


def faz_requisicao(sock, requisicao):
    '''Faz uma requisição ao servidor e exibe o resultado.
    Entrada: socket conectado ao servidor'''
    # le as mensagens do usuario ate ele digitar 'fim'

    sock.send(requisicao.encode('utf-8'))

    # espera a resposta do servidor
    msg = sock.recv(1024)

    # imprime a mensagem recebida
    print(str(msg, encoding='utf-8'))


# código da interface de usuário,


def print_interface():
    global modo
    os.system(clear)
    print("Bem vindo ao sistema de dicionário de remoto")
    print("Neste sistema, você pode registrar uma chave e um texto, ou você pode consultar o texto de uma chave existente")
    print("1 - Registrar chave e texto")
    print("2 - Consultar chave")
    print("3 - sair")

    entrada = input("Digite o número da sua escolha: ")

    # enquanto entrada não for um número, ou for um número fora das escolhas possíveis
    while True:
        try:  # usando try except porque se a entrada não for um número, o cast para inteiro ira causar uma exception
            entrada = int(entrada.strip())
            if entrada <= 3 and entrada >= 1:
                modo = entrada
                break
            else:
                entrada = input("Por favor, digite uma opção válida: ")
        except Exception as e:
            entrada = input("Por Favor, digite o número da sua escolha: ")

    return


def print_consulta(sock):
    global modo
    os.system(clear)
    print("Você está consultando. Para retornar a tela inicial, apenas entre com uma string vazia")

    # enquanto a string não for vazia, tentaremos consultar chaves
    while True:
        entrada = input("Digite a chave que deseja consultar: ")
        if not entrada:
            break
        metodo = 'g'  # metodo de requisição, g é referência a get
        requisicao = f'{metodo}{entrada}'

        # com a requisição formada, podemos finalmente fazer
        faz_requisicao(sock, requisicao)

    modo = 0
    # volta para a tela inicial
    return


def print_registro(sock):
    global modo
    os.system(clear)
    print("Você está registrando. Para retornar a tela inicial, apenas entre com uma string vazia")
    # enquanto a string não for vazia, tentaremos registrar
    while True:
        entrada = input(
            "Digite a chave seguidade de espaço e o texto que deseja inserir: ")
        if not entrada:
            break
        # if len(entrada.split(maxsplit=1)) < 2:
            # print("Valo")
            # continue
        metodo = 'p'  # metodo de requisição, p é referência a post
        requisicao = f'{metodo}{entrada}'
        faz_requisicao(sock, requisicao)
    # volta para a tela inicial
    modo = 0
    return


def main():
    '''Funcao principal do cliente'''
    # inicia o cliente
    sock = iniciaCliente()
    # interage com o servidor ate encerrar

    while modo != 3:
        if modo == 0:
            print_interface()
        if modo == 1:
            print_registro(sock)
        if modo == 2:
            print_consulta(sock)

    # encerra a conexao
    sock.close()


if __name__ == '__main__':
    main()
