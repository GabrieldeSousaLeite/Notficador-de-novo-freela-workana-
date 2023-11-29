# Notficador-de-novo-freela-workana
Versão Final Sem Interface

Esse notificador independe de requisições para o site Workana, logo, o fluxo de funcionamente (moderadamente) não é barrado.

Não fiz testes mais específicos, mas o uso ideal é de uma em uma hora.

Durante o uso, é criada uma pasta imagens onde ficaram as prints dos últimos 3 novos freelas, e tabém é criado um banco de dados SQLite 'Workana' com uma tabela 'freelas'.

Basicamente, é aberto um web driver Crhome invisível com a biblioteca Selenium, o bot do script realiza ações igual um usuário comum.
O objetivo é limpar os objetos na janela e tirar prints dos 3 primeiros novos projetos, sendo cada projeto transformado opticamente em texto.
O texto gerado é armazenado em um banco de dados SQLite, para que seja possivél comparar os novos projetos com os antigos, garantido que os novos sejão realmente novos, e não repetições.
Caso seja realmente novo, o texto é trasformado em notificação com um alerta sonoro através da bibliteca Winotify.

Para que o código funcione, é necessario passar o caminho do tesseract.exe na linha 100 que precisa estar instalado em seu pc, fora a instalação das outras bibliotecas e suas dependências.
Para personalização dos filtros de pesquisa de projetos na workana, é necessário copiar o link do site com os filtros já aplicados na pesquisa e colar na linha 49, que já conterá um link referência.

CONDIÇÕES DE USO:
Python 3.12.0
Compilador C++ Vscode ou semelhante
