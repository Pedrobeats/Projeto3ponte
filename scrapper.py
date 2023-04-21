import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm


# Análise do Fluxo de Veículos da Terceira Ponte #

def scrapper_3ponte():
    # Baixar as bases de Dados do Site de Dados Abertos do Governo do Espírito Santo: \
    # https://dados.es.gov.br/dataset/portal-da-transparencia-fluxo-de-veiculos-rodosol

    # Requests na Página e dando parsing com o BeautifulSoup
    def pegar_codigo():
        url = 'https://dados.es.gov.br/dataset/portal-da-transparencia-fluxo-de-veiculos-rodosol'
        response = requests.get(url)
        html = response.content
        global dados
        dados = BeautifulSoup(html, 'html.parser')
        return dados

    # Pegando os links da Página
    def pegar_links_csv():
        links = dados.find_all("a", class_="resource-url-analytics")
        global lista_links
        lista_links = []
        for link in tqdm(links, desc='Copiando links'):
            href = link.get("href")
            lista_links.append(href)
            time.sleep(0.2)
        return lista_links

    # Abrindo os links no pandas
    def importando_csv_pandas():
        global df
        df = pd.DataFrame()
        for item in tqdm(lista_links, desc='Adicionando o arquivo na Dataframe'):
            try:
                # Lendo o arquivo CSV e adicionando ao DataFrame
                temp_df = pd.read_csv(item, sep=';')
                df = pd.concat([df, temp_df], ignore_index=True)
                time.sleep(0.2)
            except Exception as e:
                print(f"Erro ao abrir o link {item}: {e}")
        print('Adição dos dados concluido')
        return df

    # Formatando e limpando a Dataframe:
    def data_datetime():
        global df
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S')
        #df['valorDia'] = df['valorDia'].apply(lambda x: x.replace(',', '.'))
        #df['valorDia'] = df['valorDia'].astype(float)
        dicionario_nomes_novos = {'categoria_1':'Automóvel, caminhonete e furgão',
                                  'categoria_2':'Caminhão leve, ônibus, caminhão-trator e furgão',
                                  'categoria_3':'Automóvel e caminhonete com semirreboque',
                                  'categoria_4':'Caminhão, caminhão-trator com semirreboque e ônibus',
                                  'categoria_5':'Automóvel e caminhonete com reboque',
                                  'categoria_6':'Caminhão com reboque, caminhão-trator com semirreboque (4 Eixos)',
                                  'categoria_7':'Caminhão com reboque, caminhão-trator com semirreboque (5 Eixos)',
                                  'categoria_8':'Caminhão com reboque, caminhão-trator com semirreboque (6 Eixos)',
                                  'categoria_9':'Motocicletas, motonetas, bicicletas moto',}
        df.rename(columns=dicionario_nomes_novos, inplace=True)
        return df

    def exportar_csv():
        df.to_csv('dados_3ponte.csv', index=False, encoding='UTF-8')

    # Executando as funções
    pegar_codigo()
    pegar_links_csv()
    importando_csv_pandas()
    data_datetime()
    exportar_csv()


scrapper_3ponte()