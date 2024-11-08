Descrição da API para Registro de Chamadas Telefônicas
Essa API foi desenvolvida para gerenciar registros detalhados de chamadas telefônicas, incluindo o momento de início e término de cada ligação, a duração e o custo associado a cada chamada, conforme regras de tarifação específicas. A API é ideal para sistemas que precisam armazenar e recuperar dados de chamadas telefônicas, com a capacidade de calcular preços com base na duração e no horário em que a chamada foi realizada.

Funcionalidades Principais
Registro de Início de Chamada:

Descrição: Armazena informações detalhadas de quando uma chamada foi iniciada, incluindo identificador da chamada, timestamp de início, número de telefone de origem e número de destino.
Endpoint: POST /api/phone_calls/start
Parâmetros:
call_id: Identificador único para a chamada.
type: Tipo do registro, sempre “start” para início de chamada.
timestamp: Data e hora em que a chamada foi iniciada.
source: Número de telefone do assinante que originou a chamada.
destination: Número de telefone para o qual a chamada foi feita.
Registro de Fim de Chamada:

Descrição: Armazena informações de quando a chamada foi encerrada, registrando o identificador e o timestamp de término.
Endpoint: POST /api/phone_calls/end
Parâmetros:
call_id: Identificador único para a chamada (deve corresponder ao ID do início da chamada para que o sistema identifique o par início/fim).
type: Tipo do registro, sempre “end” para fim de chamada.
timestamp: Data e hora em que a chamada foi encerrada.
Consulta de Tarifação:

Descrição: Permite a consulta de registros tarifados de chamadas feitas por um determinado número de telefone em um período de tempo especificado. A consulta retorna informações como o número de destino, timestamps de início e término da chamada, duração e o preço calculado para a chamada.
Endpoint: GET /api/phone_calls/search
Parâmetros de Consulta:
source: Número de telefone do assinante que originou as chamadas.
timeframe: Período de tempo para a busca, no formato AAAA-MM (exemplo: 2024-03 para março de 2024).
Exemplo de Resposta de Consulta de Tarifação
json
Copy code
{
  "call_id": 72,
  "destination": "11987654321",
  "start_timestamp": "2024-11-03T10:15:30.000+00:00",
  "end_timestamp": "2024-11-03T10:19:30.000+00:00",
  "call_duration": "4m0s",
  "call_price": 0.72
}
Regras de Tarifação
A API utiliza uma lógica de tarifação baseada em dois períodos distintos:

Tarifa Normal: Das 6h às 22h, com uma taxa fixa de R$ 0,36 e R$ 0,09 por minuto (somente para ciclos completos de 60 segundos).
Tarifa Reduzida: Das 22h às 6h, com uma taxa fixa de R$ 0,36 e sem cobrança adicional por minuto.
Estrutura dos Dados
Os dados são armazenados em um banco de dados MongoDB, estruturado em duas coleções:

Coleção de Início de Chamadas: Armazena registros de chamadas com informações de origem, destino e timestamp de início.
Coleção de Tarifação: Armazena registros de tarifação calculada para cada chamada, com informações de duração e custo, além do timestamp de início e término.
Tecnologias Utilizadas
Backend: Desenvolvido em Python com o framework Flask.
Banco de Dados: MongoDB, que oferece flexibilidade e escalabilidade para armazenar registros detalhados de chamadas.
Hospedagem: A API pode ser hospedada em provedores como Heroku, com variáveis de ambiente configuradas para o URI do MongoDB e a porta dinâmica.
Exemplo de Uso
Registrar uma Chamada: Enviar uma solicitação POST para o endpoint de início de chamada com os detalhes da chamada.
Encerrar uma Chamada: Enviar uma solicitação POST para o endpoint de término de chamada, usando o mesmo call_id para associar o fim ao início da chamada.
Consultar Chamadas Tarifadas: Usar o endpoint de consulta para verificar o histórico de chamadas, informando o número de origem e o período desejado. A resposta inclui o preço calculado para cada chamada registrada.
Essa API foi projetada para oferecer uma solução robusta e flexível para o gerenciamento e tarifação de chamadas telefônicas, com fácil integração em sistemas de telecomunicações ou plataformas de CRM que necessitam de gerenciamento detalhado de registros de chamadas.

Instruções do Projeto
1. Instalação do Python e Preparação do Ambiente
Instale o Python:

Baixe o instalador do Python na página oficial (versão 3.9 ou superior).
Durante a instalação, marque a opção "Add Python to PATH" para facilitar o acesso ao Python pelo terminal.
Verifique a Instalação:

Após a instalação, abra o terminal (Prompt de Comando, PowerShell, ou terminal do VS Code) e verifique a versão:
bash
Copy code
python --version
Isso deve exibir a versão do Python instalada (por exemplo, Python 3.9.7).
Instale o pip (caso ainda não esteja instalado):

pip é o gerenciador de pacotes do Python e, geralmente, já vem incluído nas versões recentes do Python. Verifique a instalação executando:
bash
Copy code
pip --version
Caso o pip não esteja instalado, consulte a documentação oficial para instruções de instalação.
2. Instalação da IDE (Visual Studio Code)
Baixe e Instale o Visual Studio Code (VS Code):

Acesse o site do Visual Studio Code e baixe a versão correspondente ao seu sistema operacional.
Instale Extensões Recomendadas:

Abra o VS Code e vá até a seção de extensões (ícone de quadrados no menu lateral ou Ctrl+Shift+X).
Pesquise e instale as seguintes extensões:
Python: Fornece suporte a sintaxe, linting e debugging para Python.
Pylance: Melhora a experiência com Python, oferecendo análise de código e autocompletar.
REST Client (opcional): Permite testar as requisições da API diretamente no VS Code, sem a necessidade de usar uma ferramenta externa.
3. Configuração do Projeto e Instalação dos Pacotes
Clone ou Baixe o Código da API:

Se o código estiver em um repositório Git, use o comando abaixo para clonar o projeto:
bash
Copy code
git clone https://github.com/seu-repositorio/nomedoprojeto.git
cd nomedoprojeto
Crie e Ative um Ambiente Virtual:

Um ambiente virtual ajuda a gerenciar as dependências do projeto isoladamente.
No terminal, dentro da pasta do projeto, crie o ambiente virtual:
bash
Copy code
python -m venv env
Ative o ambiente:
Windows:
bash
Copy code
.\env\Scripts\activate
macOS/Linux:
bash
Copy code
source env/bin/activate
Instale as Dependências do Projeto:

As dependências estão listadas no arquivo requirements.txt. Para instalar todas de uma vez, execute:

bash
Copy code
pip install -r requirements.txt
Este comando instalará pacotes como Flask, pymongo, flask-restx, entre outros, necessários para o funcionamento da API.

4. Configuração do Banco de Dados (MongoDB Atlas)
Crie uma Conta no MongoDB Atlas:

Acesse MongoDB Atlas e crie uma conta.
Configure o Cluster e Banco de Dados:

No Atlas, crie um novo cluster e configure um banco de dados (por exemplo, Call).
Na seção de Network Access, permita o acesso de todos os IPs (0.0.0.0/0).
Obtenha a URI de Conexão:

No Atlas, copie a URI de conexão. Ela terá o seguinte formato:
plaintext
Copy code
mongodb+srv://<username>:<password>@cluster0.mongodb.net/Call?retryWrites=true&w=majority
Substitua <username> e <password> pelo seu nome de usuário e senha do MongoDB Atlas.
Configure a Variável de Ambiente MONGO_URI:

No arquivo .env na raiz do projeto (crie um, se necessário), adicione a URI de conexão:
plaintext
Copy code
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/Call?retryWrites=true&w=majority"
Carregue o .env no Projeto:

Verifique se o código está configurado para carregar variáveis de ambiente do .env usando a biblioteca dotenv no Python, no início do seu arquivo principal (ex: main.py):
python
Copy code
from dotenv import load_dotenv
load_dotenv()
5. Executando e Testando a API Localmente
Inicie o Servidor Local:

Com o ambiente virtual ativo, execute o seguinte comando para iniciar a API:
bash
Copy code
python main.py
A API deve rodar no endereço http://127.0.0.1:5000 por padrão.
Acesse a Documentação Swagger:

Abra o navegador e acesse http://127.0.0.1:5000/docs ou http://127.0.0.1:5000/api/phone_calls para visualizar a documentação da API.
Teste os Endpoints:

Use um cliente REST como o Postman, Insomnia ou a extensão REST Client no VS Code para enviar requisições HTTP aos endpoints.
Exemplos de testes:
Iniciar uma Chamada:

http
Copy code
POST http://127.0.0.1:5000/api/phone_calls/start
Content-Type: application/json

{
    "call_id": 1,
    "type": "start",
    "timestamp": "2024-11-08T10:00:00",
    "source": "11912345678",
    "destination": "11987654321"
}
Encerrar uma Chamada:

http
Copy code
POST http://127.0.0.1:5000/api/phone_calls/end
Content-Type: application/json

{
    "call_id": 1,
    "type": "end",
    "timestamp": "2024-11-08T10:30:00"
}
Consultar Chamadas Tarifadas:

http
Copy code
GET http://127.0.0.1:5000/api/phone_calls/search?source=11912345678&timeframe=2024-11
Verifique os Logs:

Durante os testes, o terminal mostrará logs das requisições. Observe os logs para garantir que tudo está funcionando corretamente e para capturar quaisquer mensagens de erro.
6. Configuração para Hospedagem (Opcional)
Para hospedar a API em uma plataforma como Heroku, siga estes passos adicionais:

Crie um Procfile:

O Procfile deve conter o comando para iniciar o app no Heroku:
plaintext
Copy code
web: python main.py
Configure as Variáveis de Ambiente no Heroku:

Defina a variável MONGO_URI no Heroku usando o CLI:
bash
Copy code
heroku config:set MONGO_URI="sua-URI-mongodb"
Implemente e Monitore a Aplicação:

Realize o push do código para o Heroku e verifique os logs para garantir que o aplicativo está rodando corretamente.
Esses passos cobrem a configuração e o teste completo do ambiente de desenvolvimento para a API.

Ambiente de Trabalho
Sistema Operacional: Windows com WSL (Windows Subsystem for Linux) habilitado, permitindo a execução de um ambiente Linux em paralelo com o sistema Windows. O WSL facilita a execução de comandos e ferramentas nativas de Linux, melhorando a compatibilidade com bibliotecas e dependências de Python.

Distribuição Linux (WSL): Ubuntu (ou outra distribuição compatível) foi usada como ambiente Linux dentro do WSL para executar os comandos e gerenciar o ambiente Python.

Editor de Texto/IDE: Visual Studio Code (VS Code), com extensões específicas para Python e desenvolvimento de APIs REST, como:

Python: Suporte a sintaxe, execução de código e análise de erros em Python.
Pylance: Ferramenta avançada de autocompletar e verificação de tipos para Python.
REST Client (opcional): Facilita o teste de requisições API diretamente no editor.
Bibliotecas e Frameworks:

Flask: Framework de microserviços para Python, usado para criar os endpoints da API.
Flask-RESTx: Extensão que facilita a documentação e estruturação de APIs RESTful.
Pymongo: Biblioteca para interação com o MongoDB, usada para conectar e manipular dados no banco de dados MongoDB Atlas.
Python-dotenv: Utilizada para carregar variáveis de ambiente do arquivo .env, incluindo a URI do MongoDB, garantindo que informações sensíveis não fiquem hardcoded no código.
Banco de Dados: MongoDB Atlas como banco de dados de armazenamento de registros de chamadas. O MongoDB Atlas é um serviço de banco de dados em nuvem que oferece fácil escalabilidade e alta disponibilidade.