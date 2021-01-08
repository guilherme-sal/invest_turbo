import requests
import pandas as pd
from bs4 import BeautifulSoup
import os


def get_stock_description():

    os.system("clear")

    print('Buscando descrição das suas ações...')
    print('\n')

    df = pd.read_csv('./tables/tabela.csv')
    stock_description_list = []

    for stock in df['SIGLA']:

        try:
            html = requests.get(f'https://finance.yahoo.com/quote/{stock}.SA?p=PETR4.SA&.tsrc=fin-srch').text
            soup = BeautifulSoup(html, 'html.parser')
            stock_description = soup.find('h1', class_='D(ib) Fz(18px)').getText()
            stock_description = stock_description.split('(')[0]
            print(stock_description)
            stock_description_list.append(stock_description)

        except Exception as e:
            print(e)
            stock_description_list.append('NaN')

    df['DESCRIÇÃO'] = stock_description_list
    df.to_csv('./tables/tabela.csv', index=False)