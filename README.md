# Repository_Books_Project
This project search showing the essentials skills that data science needed in the day for process ETL.
# DOCUMENTAÇÃO DA SOLUÇÃO
### Para início de contextualização este projeto serve como uma simulação de um problema real de engenharia de dados para conseguir mostrar habilidades de scraping, databases e capacidade analítica.
 	O que de fato se tem como objetivo é trazer parte da construção de um projeto de engenharia de dados, pois muitas vezes são necessárias estas habilidaes para o cientista de dados em seu ambiente(na ausência de um engenheiro)

### Este trabalhon serve como uma demosntração de habilidades que estão sendo aprendidas ao longo dos estudos de ciência de dados e suas aplicações.
	O projeto foi feito numa máquina com:
	- Sistema W11 e WSL - Linux
	- 8 GB RAM, 256 GB SSD e Processador AMD 5-5500U

### Como ocorreu o contexto do projeto?

	Este projeto é baseado no blog Seja um Data Science e foi construído a partir uma história fictícia com o seguinte enredo:
	"Contexto do Desafio:
	A Book Club é uma Startup de troca de livros. O modelo de negócio funciona com base na troca de livros pelos usuários, cada livro cadastrado pelo usuário, dá o direito à uma troca, porém o usuário também pode comprar o livro, caso ele não queira oferecer outro livro em troca.

	Umas das ferramentas mais importantes para que esse modelo de negócio rentabilize, é a recomendação. Uma excelente recomendação aumenta o volume de trocas e vendas no site.

	Você é um Data Scientist contrato pela empresa para construir um Sistema de Recomendação que impulsione o volume de trocas e vendas entre os usuários. Porém, a Book Club não coleta e nem armazena os livros enviados pelos usuários.

	Os livros para troca, são enviados pelos próprios usuários através de um botão “Fazer Upload”, eles ficam visíveis no site, junto com suas estrelas, que representam o quanto os usuários gostaram ou não do livro, porém a Startup não coleta e nem armazena esses dados em um banco de dados.

	Logo, antes de construir um sistema de recomendação, você precisa coletar e armazenar os dados do site. Portanto seu primeiro trabalho como um Data Scientist será coletar e armazenar os seguintes dados:

	O nome do livro.
	A categoria do livro.
	O número de estrelas que o livro recebeu.
	O preço do livro.
	Se o livro está em Estoque ou não."


# SOLUÇÃO DO PROJETO:

**EXTRAÇÃO DE SCRAPING**

	 A ideia do extração foi bem simples: Puxar dados de páginas e navegar entre elas sempre clicando no botão de próximo(se houver) e então conseguir extrair os dados de cada página
	 até que não haja mais próximo e então de passa para a próxima categoria de livros.

**BANCO DE DADOS CONFIGURAÇÃO E ARMAZENAMENTO DE DADOS**
	
	  Para o banco de dados foi necessário usar o postgres dentro de uma WSL já que posteriormente iria-se usar Apache Airflow, por isso após a extração dados e tratamento dos mesmos usou-se
	  bibliotecas do python para importar os dados extraídos para o banco de dados postgres.

**AUTOMAÇÃO DE PIPELINE DE DADOS**
	
	Na automação foi necessário a configuração do sistema WSL(pois a maioria dos tutoriais completos era feitos em sistema linux), daí modularizou-se as funções python para que conseguissem
	que se fosse possível chamá-las a partir de DAGS para construção do pipline de ETL.

## PROBLEMAS RELATADOS QUE FORAM DIFÍCEIS DE SOLUCIONAR

**Problema com o airflow venv**
	
	Solução para configuração do chrome driver in wsl
	O que solucionou o problema!
	https://stackoverflow.com/questions/64717302/deprecationwarning-executable-path-has-been-deprecated-selenium-python

	https://stackoverflow.com/questions/46026987/selenium-gives-selenium-common-exceptions-webdriverexception-message-unknown

	https://stackoverflow.com/questions/33382998/chromedriver-various-lib-dependencies-are-missing-on-ubuntu-14-04-64-bit

**Problema com agendamento do script:**
	
	SOLUÇÃO:
	export AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=300

**Comando de derrubar processo de porta linux:(Necessidade caso fosse necessário resatar o servidor apache para puxar novas configurações)**
	
	fuser -k 8080/tcp
	Se não houver fuser use o comando: sudo apt-get install psmisc 
		sudo service postgresql start # CONECTANDO BANCO DE DADOS POSTGRESQL
		sudo service postgresql stop # FECHANDO CONEXÃO COM BANCO DE DADOS POSTGRESQL

**SE VOCÊ FOR EXECUTAR UMA AÇÃO SUDO NO AIRFLOW VOCÊ DEVE DEFINIR UMA AIRFLOW(PERMISSÃO SEM SENHA DE USUÁRIO LINUX)**
	
	https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/security/workload.html
	Ensina a achar o arquivo para sudo
	(https://medium.com/@jimmashuke/how-to-stop-that-annoying-sudo-password-prompt-in-linux-b2b72b9c2f55)
	OBS>>  Você deve descorbir quem é o usuário que irá executar seu trabalho no airflow para saber qual é este basta digitar: *id* e verificar o user

