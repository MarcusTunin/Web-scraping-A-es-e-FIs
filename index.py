import mysql.connector
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np


MYSQLHOST = "localhost"
MYSQLPORT = 3306
MYSQLUSER = "usuario do banco"
PASS = ""
DATABASE = "tabela_banco"

try:
    conn = mysql.connector.connect(
        host=MYSQLHOST,
        port=MYSQLPORT,
        user=MYSQLUSER,
        password=PASS,
        database=DATABASE
    )
    cursor = conn.cursor()
    print("Conexão bem-sucedida ao banco de dados MySQL")

except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")
    exit()

# Variável do ativo
ativo = "ativo desejado" #EX: mxrf11

# Iniciar o navegador e acessar a URL do ativo
navegador = webdriver.Chrome()
url_moeda = "https://statusinvest.com.br/fundos-imobiliarios/" + ativo
navegador.get(url_moeda)

# Requisição para buscar o nome do ativo
name = navegador.find_element(By.CSS_SELECTOR,"#main-header > div.container.pl-2.pr-1.pl-xs-3.pr-xs-3 > div > div:nth-child(1) > div > ol > li:nth-child(3) > a > span").text
name = name.split()
tabela_ativo = pd.DataFrame(name, columns=["Ativo"])
print(tabela_ativo)

# Coletar dados do ativo
dividend_yeld = navegador.find_element(By.CSS_SELECTOR,"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(4) > div > div:nth-child(1) > strong").text
dividend_yeld = dividend_yeld.split()
p_vp = navegador.find_element(By.CSS_SELECTOR,"#main-2 > div.container.pb-7 > div:nth-child(5) > div > div:nth-child(1) > div > div:nth-child(1) > strong").text
p_vp = p_vp.split()
valor_atual = navegador.find_element(By.CSS_SELECTOR,"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong").text
valor_atual = valor_atual.split()
data_ultimo_rendimento = navegador.find_element(By.CSS_SELECTOR,"#dy-info > div > div:nth-child(2) > div:nth-child(3) > div:nth-child(2) > div > b").text
data_ultimo_rendimento = data_ultimo_rendimento.split()
valor_ultimo_rendimento = navegador.find_element(By.CSS_SELECTOR,"#dy-info > div > div.d-flex.align-items-center > strong").text
valor_ultimo_rendimento = valor_ultimo_rendimento.split()
liquidez_media_diaria = navegador.find_element(By.CSS_SELECTOR,"#main-2 > div.container.pb-7 > div:nth-child(6) > div > div > div.info.p-0 > div > div > div > strong").text
liquidez_media_diaria = liquidez_media_diaria.split()
print(valor_atual)


#Inserir dados no banco
insert_query = """
INSERT INTO fundos_imobiliarios (nome_ativo, dividend_yeld, p_vp, valor_atual, data_ultimo_rendimento, valor_ultimo_rendimento, liquidez_media_diaria)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""
cursor.execute(insert_query, (name[0], dividend_yeld[0], p_vp[0], str(valor_atual[0]), data_ultimo_rendimento[0], valor_ultimo_rendimento[0], liquidez_media_diaria[0]))
conn.commit()

print("Dados inseridos com sucesso!")

# Fechar a conexão
cursor.close()
conn.close()
navegador.quit()
