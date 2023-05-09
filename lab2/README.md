# Lab 2:

## Parte 1:
Entendendo o objetivo do sistema, é bem notável enxergar que é ele pode ser caracterizado como um sistema de informação distribuído.

Dito isto, seguindo a tradicionalidade, uma ótima escolha de estilo arquitetural para projetarmos seria a arquitetura em camadas.

Onde teremos as seguintes camadas:
Camada de Aplicação(interface de usuário)

Camada de Processamento(processamento das requisições pelo lado do servidor)

Camada de dados(Acesso e persistência do nosso dicionário)


especificando os componentes:

A camada de aplicação, seria responsável pelos seguinte componente: 
1 - Interface de usuário

(Pensando em uma boa modularização, poderia valer a pena dividir a interface de usuário em componentes menores, mas por ser um sistema simples, escolhi não fazer isso)

A camada de processamento seria responsável pelos seguintes componentes:
1 - Processamento de requisição
2 - Remoção de dados

(A remoção de dados poderia também estar em uma "segunda camada de aplicação", que estaria disponível apenas no lado do processamento. Por escolha pessoal, decidi deixar na camada de processamento, já que é uma forma de requisição direta no servidor)

Por fim, a camada de dados, que é responsável pelos seguintes componente:

1- Acesso e persistência do dicionário

(Ainda pensando em uma boa modularização, também valeria a pena dividir em componentes menores. Mas optei por não fazer isso, pois esta camada apenas irá realizar o que a camada de processamento pedir e a sua implementação seja pelo sistema de arquivos ou por um sgbd, camada acaba ficando "obscura" para nós).

A comunicação seria da seguinte forma:
A camada de aplicação envia uma requisição através para a camada de processamento.
A camada de processamento envia uma requisição para a camada de dados.
Então a camada de dados responde para a de processamento, que responde para a de aplicação.
(Excessão sendo o componente de remoção, que não responde pra ninguém, pois é iniciado diretamente no processamento)

A camada de aplicação pode iniciar um contato com a camada de processamento, mas a de processamento não pode iniciar um contato com a de aplicação.

A camada de processamentos pode iniciar um contato com a camada de de dados, mas a de dados não pode iniciar um contato nem com a de processamento, nem a de aplicação. Então a regra desta arquitetura está "obedecida" 




## Parte 2:

2:

Levando agora para a arquitetura de sistema cliente/servidor, de 2 níveis:
O lado do cliente cuidará da camada de aplicação

O lado do servidor cuidará da camada de processamento e da camada de dados

A cama de dados será um arquivo local, então neste caso será gerenciado pelo próprio sistema de arquivos.

O cliente ao rodar o programa terá uma interface com 3 opções
Consultar, registrar e sair
Sair irá encerrar a conexão
Consultar irá enviar uma requisição de consulta de chave
Registrar irá enviar uma requisição de registro de chave

O servidor, ao receber requisição, irá processá-la.
Primeiro irá verificar que tipo de requisição é.
Se for uma requisição de consulta, irá acessar a api do sistema de arquivos para carregar o dicionário e mostrar a chave.
Se for de registro, irá acessar a api do sistema de arquivos para sobreescrever o dicionário.

Após isso, o servidor deve responder para o cliente:
Em caso de requisição de consulta: Valor da chave encontrada ou "Chave não encontrada"
Em caso de registro: Par chave valor inserido ou par chave valor atualizado.
Então, depois de receber sua resposta, o cliente poderá fazer outra requisição, ou finalizar o sistema

Além disso, diretamente pelo servidor, se o administrador entrar com um comando de remover, o servidor também irá acessar a api do sistema de arquivos para sobreescrever o dicionário, sem a chave a removida e informar o administrador se a chave foi removida com sucesso ou não.

## Parte 3:
O código está bem comentado e as modularizações estão bem explicativas, então vou focar em explicar as decisões principais:

Começando pelo lado do cliente.
Este lado possui 4 modos, sendo 3 deles telas e um deles a opção de sair.
0 é tela inicial, 1 é registro, 2 é consultar e 3 é finalizar o sistema

A tela inicial deixa o usuário escolher outras opções
A tela de registro deixa o usuário registrar chaves
A tela de consultas deixa o usuário consultar chaves

Nessas telas, o usuário pode fazer quantas requisições quiser, e quando quiser sair, basta apertar enter sem digitar nada.
Quando o usuário faz uma requisição, dependendo do "modo" em que ele estiver, automaticamente será concatenado um caracter com a string de entrada.

Por exemplo, se ele estiver na tela de consultas, e quiser consultar a chave "Arroz", a requisição ficará gArroz
Este g é tem eset nome por causa do método GET.
A mesma coisa acontecerá se ele estiver na tela de registro, mas com um 'p' por causa do Método POST
Então se o usuário quiser registrar a chave Arroz com o valor Feijão, a requisição irá ficar pArroz Feijão.
Por escolha de design, na hora de registrar uma chave, o conteúdo entre chave e valor será separado por um espaço, então a requisição
Arroz Feijão com Farofa irá guardar a chave Arroz, e o valor Feijão com Farofa.

Indo agora para o lado do servidor, que irá receber essa requisição e irá verificar o primeiro caracter da string, para saber é uma consulta ou um registro.
A partir daí o servidor decide se deverá inserir ou buscar uma chave no dicionário.
O dicionário é salvo e carregado de um arquivo json chamado dicionario.json, que fica na mesma pasta onde o servidor.py roda. Se o dicionario.json não existir, o servidor cria um vazio.
E claro, o servidor também está disponível para receber comandos do admnistrador. remover 'chave' para remover uma chave e seu valor do dicionário e também fim para finalizar o servidor quando todas as threads de conexões houverem terminado.

Além dos testes normais para verificar se os componentes funcionavam. Foram realizados vários testes ao longo do desenvolvimento para garantir o funcionamento aceitável, tais como tentativas de inserção com valor vazio, remoção com valor vazio, consulta de chave vazia, escolha de modos inválidos, etc. 
