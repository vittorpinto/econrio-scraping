#%% Importações
import requests
from bs4 import BeautifulSoup
import os
import re

#%% Função para buscar página
def buscar_pagina(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Erro ao acessar a página: {response.status_code}")
        return None

#%% Função para extrair os links da página principal (processos seletivos)
def extrair_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    div_container = soup.find('div', {'class': 'et_pb_ajax_pagination_container'})
    links = []
    
    if div_container:
        # Extrair links de todos os artigos dentro do div
        for article in div_container.find_all('article'):
            link = article.find('a')['href']
            links.append(link)
    else:
        print("Div container não encontrado.")
    
    return links

#%% Função para baixar um arquivo
def baixar_arquivo(url, diretorio):
    response = requests.get(url)
    nome_arquivo = os.path.join(diretorio, url.split('/')[-1])
    with open(nome_arquivo, 'wb') as f:
        f.write(response.content)
    print(f"Arquivo salvo em: {nome_arquivo}")

#%% Função para criar um diretório com base no título ou URL
def criar_diretorio_para_pagina(url, titulo):
    # Limpar o título ou URL para ser um nome de pasta válido
    if not titulo:
        titulo = re.sub(r'https?://|www\.|[^A-Za-z0-9]+', '_', url)  # Usar o URL se não houver título
    else:
        titulo = re.sub(r'[^A-Za-z0-9]+', '_', titulo)  # Limpar caracteres inválidos no título

    diretorio_pagina = os.path.join("./arquivos_provas", titulo)
    os.makedirs(diretorio_pagina, exist_ok=True)
    return diretorio_pagina

#%% Função para extrair e baixar links de provas das páginas específicas
def extrair_e_baixar_links_provas(html, diretorio, headers):
    soup = BeautifulSoup(html, 'html.parser')

    # Termos a procurar nos parágrafos que indicam "Provas"
    termos_prova = ['Prova', 'Provas', 'Provas e Gabaritos', 'Vestibulares anteriores']
    
    for p in soup.find_all('p'):
        if any(termo in p.get_text() for termo in termos_prova):
            print(f"Encontrado parágrafo: {p.get_text()}")
            
            # Encontrar o próximo elemento que contenha os links (geralmente <ul>)
            proximo_elemento = p.find_next_sibling()
            
            if proximo_elemento and proximo_elemento.name == 'ul':
                # Extrair links da lista <ul>
                for link in proximo_elemento.find_all('a', href=True):
                    url_arquivo = link['href']
                    
                    # Verificar se o link é uma página intermediária ou um arquivo direto
                    if url_arquivo.endswith('.pdf'):
                        # Se for um arquivo direto, baixa o arquivo
                        print(f"Baixando arquivo: {url_arquivo}")
                        baixar_arquivo(url_arquivo, diretorio)
                    else:
                        # Se for uma página intermediária, acessa e busca provas nela
                        print(f"Acessando página intermediária: {url_arquivo}")
                        html_intermediaria = buscar_pagina(url_arquivo, headers)
                        if html_intermediaria:
                            extrair_e_baixar_links_provas(html_intermediaria, diretorio, headers)
                        else:
                            print(f"Erro ao acessar a página intermediária: {url_arquivo}")
            else:
                print("Nenhuma lista de links foi encontrada após o parágrafo.")

#%% Cabeçalhos da requisição
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,pl;q=0.6',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

# URL da página principal (processos seletivos)
url_pagina = "https://econrio.com.br/index.php/processosseletivos/"
html = buscar_pagina(url_pagina, headers)

# Criando diretório principal para salvar os arquivos
diretorio_principal = "./arquivos_provas"
os.makedirs(diretorio_principal, exist_ok=True)

# Se a página principal foi carregada com sucesso, vamos extrair os links
if html:
    links_provas = extrair_links(html)
    
    # Para cada link da página principal, acessar e procurar por provas e gabaritos
    for link in links_provas:
        print(f"Acessando a página: {link}")
        pagina_prova_html = buscar_pagina(link, headers)
        
        if pagina_prova_html:
            # Extraindo o título da página para nomear a pasta
            soup = BeautifulSoup(pagina_prova_html, 'html.parser')
            titulo_pagina = soup.title.string if soup.title else None
            
            # Criando uma pasta para essa página específica
            diretorio_pagina = criar_diretorio_para_pagina(link, titulo_pagina)
            
            # Extraindo e baixando os links de provas
            extrair_e_baixar_links_provas(pagina_prova_html, diretorio_pagina, headers)
        else:
            print(f"Erro ao acessar a página: {link}")
else:
    print("Erro ao carregar a página principal.")

# %%
