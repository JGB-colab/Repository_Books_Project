from bs4 import BeautifulSoup as bs
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import psycopg2 as pg

class scraper():

    # instancia link de página
    def __init__(self,link):
        self.link = link
    # Ação: Checar se existe mais de uma página de navagação
    def puxar_dados_livros(self,struture_html,categoria = '', estrela = '',titulo = '',valor='',estoque = ''):
        self.estrela = estrela
        self.titulo = titulo
        self.valor = valor
        self.estoque = estoque
        self.categoria = categoria
        global vetor_categorias
        vetor_categorias = []
        self.struture_html = struture_html
        parse = bs(self.struture_html,'html.parser')
        info = parse.findAll('li',attrs = {'class':"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
        # CRIAR GET DAS ESTRUTURAS
        for info_livro in info:
            self.estrela = info_livro.findAll('p')[0]['class'][1] # atributo de estrela
            self.titulo = info_livro.findAll('h3')[0].find('a')['title'] 
            self.valor = info_livro.findAll('p')[1].text
            self.estoque = info_livro.findAll('p')[2].text.replace('\n','').replace('  ','')
            vetor_categorias.append([self.estrela,self.titulo,self.valor, self.estoque])
        return vetor_categorias

    # criação de arquivo csv
    def cria_csv(self, nome,linhas):
        self.linhas = linhas
        self.nome = nome
        file = open('{0}.csv'.format(self.nome),'w',newline = '',encoding='utf-8')
        w = csv.writer(file,delimiter=';')
        for texto in self.linhas:
            w.writerow(texto)
        file.close()
    # importação para banco de dados
    def importar_banco():
        conn = pg.connect(dbname="livros", user="postgres",host="localhost",port=5432)
        arquivo = open(r'repositorio.csv','r',encoding='utf-8')
        cur = conn.cursor()
        cur.copy_from(arquivo,'livros',sep=';')
        arquivo.close()
        conn.close()

    # Executor de scraping de livros
    def scraping_livros():
        home = 'http://books.toscrape.com/index.html'
        raiz = 'http://books.toscrape.com/'
        response = requests.get(home)
        content = response.content
        site = bs(content,'html.parser')
        referecias = site.find('ul',attrs={'class':"nav nav-list"})
        # Define o driver
        options = Options()
        options.add_argument('--headless')
        options.add_argument("–no-sandbox")
        options.add_argument("–disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        # Puxando categorias que serão puxadas os dados
        categorias = []
        for ref in referecias.find_all('a'):
            categoria = ref.text.replace('\n','').replace(' ','')
            categorias.append({categoria:ref['href']})
        # Navegando pelas categorias
        repositorio = []
        for refs in categorias[1:]:
            generos = str(list(refs.keys())[0])
            endpoint = scraper(list(refs.values())[0])
            estado =  True
            driver.get(raiz +'/' + endpoint.link)
            instancia = driver.find_elements(By.TAG_NAME,'a')
            # Extraindo informações das páginas
            while estado:
                linhas_csv = endpoint.puxar_dados_livros(driver.page_source)
                for linhas in linhas_csv:
                    repositorio.append([generos] + linhas)
                    print([generos] + linhas)
                instancia =  driver.find_elements(By.TAG_NAME,'a')
                if instancia[-1].text =='next':
                    instancia[-1].click()
                else:
                    estado = False
        # Criar arquivo csv
        endpoint.cria_csv(nome = 'repositorio',linhas = repositorio)
