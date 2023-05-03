## Como rodar o projeto:
- ter o python na versão 3.6.7 instalado
- rodar os seguintes comandos no cmd:
```  
    python -m venv env
    .\env\Scripts\Activate.bat
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver	
``` 
	  	
## Objetivo do projeto:
 O projeto é uma plataforma chamada YIELD, onde o usuário pode comparar os dados, de algumas opções de ativos, com a rentabilidade de 1 ano do projeto escolhido, pois, API do desafio não forneceu um histórico de rentabilidade propriamente dito. Logo, a ideia é ter uma dimensção de quando o ativo ultrapassou ou não aquela rentabilidade de um ano em pequeno, médio ou logo prazo, podendo dar uma ideia, supondo uma rentabilidade constante, ao usuário se aquela rentabilidade faz ou não sentido para ele comparando com outros tipos de ativos.

 ## Documentação: 

 ### home: 
Pega o valor digitado no filtro de nome do projeto e testa quais projetos serão mostrados, cria o objeto Paginator, pega a página atual e retorna o valor para ser usado no template pages/home.html
 
 ### page_create: 
Chama o template que renderiza a página de criação de projeto create_project.html

 ### populate_database: 
Faz um request para a API de listagem de projetos e salva no banco de dados cada projeto em uma linha da tabela e redireciona para a página home, o botão que chama essa função só é renderizado se não houverem dados na tabela.

 ### delete_database: 
Função criada para fins de teste, a qual deleta todos os dados da tabela e retorna para a página home.

 ### create: 
Pega os dados fornecidos pelo template create_project.html e
 adiciona estes dados em uma nova linha do banco de dados e redireciona para a página home.

### edit: 
Busca no banco qual projeto possui o mesmo id fornecido na url edit/<int:id> e chama o template que renderiza a página de edição de projeto pages/update.html

### update: 
Busca no banco qual projeto possui o mesmo id fornecido na url update/<int:id> e redireciona para a home.

### delete: 
Busca no banco qual projeto possui o mesmo id fornecido na url update/<int:id>, deleta da tabela do banco e redireciona para a home.

### compare: 
Busca no banco qual projeto possui o mesmo id fornecido na url compare/<int:id>, chama a variável global do período selecionado e traduz ele para ser utilizado na yfinace, se a variável global do ativo selecionado for diferente de vázio chama a yfinace com o ativo e período escolhidos pega a data inicial e final das cotações do ativo e calcula a porcentagem de valorização do ativo, e por fim se o projeto possuir latitude e longitude, chama a geopy e traduz para endereço as coordenadas do projeto e renderiza o template pages/compare.html

### compare_stock: 
Busca no banco qual projeto possui o mesmo id fornecido na url compare_stock/<int:id>, declara as variáveis globais de filtragem do gráfico que receberão os valores escolhidos nos selects da página de comparação e redireciona para a pagina de comparação.

## Processo de desenvolvimento:     
Inicialmente, me dediquei a aprender como utilizar o framework Django, incluindo seus padrões de projeto e principais funcionalidades, como a criação de páginas, rotas e estilização. Dado o limite de tempo, decidi usar o Bootstrap 5 por ser uma forma eficiente de estilizar a aplicação e integrá-la com o Django.

Em seguida, concentrei-me em como utilizar e alterar as informações da API, as quais foram fornecidas pelo desafio, com o objetivo de criar um CRUD com os dados fornecidos. Para isso, criei uma rota para puxar esses dados via requests do Python e uma migration para criar a tabela de projetos. Adicionei um botão para popular os dados e, para fins de teste, outro botão comentado no arquivo de templates/pages/home da linha 15 até a 19, pois tendo um banco de dados eu posso alterar os dados precisando puxar da API apenas uma vez. Para isso preferi utilizar outra maneira de armazenamento ao invés da tela de admin, então utilizei como visualizador de banco o SQLite Viewer, já que os comandos são mais intuitivos e próximos aos comandos do ORM Prisma, o qual já utilizei anteriormente.

Com os dados disponíveis, criei funções de edição, deleção e criação de projetos, onde a principal dificuldade foi entender como o Django captura os dados fornecidos pelo usuário nos inputs dos templates.

Em seguida, quis mostrar ao usuário na página de comparação as informações do projeto, incluindo o endereço. Para isso, utilizei a biblioteca Geopy para decodificar a latitude e a longitude fornecida nos dados do desafio e dividi a string do endereço para fornecer as informações principais.

Meu objetivo principal era comparar a rentabilidade dos ativos. Inicialmente, tentei utilizar a biblioteca Investpy, que possui uma função search_quotes, onde não é necessário saber o nome completo do ativo e sim uma parte dele, porém, não consegui instalar de maneira correta, então utilizei a mais tradicional Yfinance.

Tendo os dados dos ativos, precisei pensar na melhor forma de plotar o gráfico de comparação, onde tentei utilizar a biblioteca Matplotlib, entretanto, a Matplotlib no Django funciona pela conversão em base64 de imagens geradas para serem exibidas nos templates e não consegui fazer o código de conversão da maneira correta então a solução foi utilizar a Chart.js.
