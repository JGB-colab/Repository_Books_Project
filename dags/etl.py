from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.bash import BashOperator
# inclusão de caminho para importar módulos python por meio de arquivo de configuração json
import sys
sys.path.insert(0,"/home/admin/airflow/scraping")
from robot_scraper import scraper
# Definindo processo de pipline de scraping dentro do airflow
def call_scraping():
    scraper.scraping_livros()
def call_import():
    scraper.importar_banco
def call_pass():
    return 'carregamento'
with DAG(
    dag_id='pipline_ws',
    start_date= datetime(2023,4,22), # Dia da criação da DAG
    schedule_interval="@hourly", # intervalo definido por sintaxe de crobtab
    catchup= False
) as dag:
    
    extract_transform = PythonOperator(
        task_id = 'extracao_transformacao',
        python_callable = call_scraping
    )
    loading = PythonOperator(
        task_id = 'carregamento',
        python_callable = call_import
    )
    init_db = BashOperator(
        task_id = 'inicia_conexao',
        bash_command= 'sudo service postgresql start'#'psql -h localhost -p 5432 -U postgres -d livros'
    )
    close_db = BashOperator(
        task_id = 'fecha_conexao',
        bash_command= 'sudo service postgresql stop'
    )
    extract_transform >> init_db  >> loading >> close_db
