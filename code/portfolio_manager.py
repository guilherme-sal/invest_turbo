import pandas as pd
import requests
import datetime
import os
from sale_function import sale_function


# CORE FUNCTIONS


def search_portfolio_list():
    df = pd.read_csv('./tables/tabela.csv')
    portfolio_list = list(df['CARTEIRA'].unique())
    portfolio_dict = {}

    for portfolio in portfolio_list:
        df_filter = df.query(f"CARTEIRA == '{portfolio}'")
        portfolio_dict.update({portfolio: df_filter})

    return portfolio_dict


def get_price_list(df):

    price_list = []

    for stock in df['SIGLA']:

        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}.SA?region=" \
                  f"BR&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=" \
                  f"finance"
            data = requests.get(url).json()
            price = data['chart']['result'][0]['meta']['regularMarketPrice']
            price_list.append(price)

        except Exception as e:
            price_list.append('NaN')

    return price_list


# CALCULATE FUNCTIONS

def calculate_proportions(df):
    quantity_proportion = df['QUANT.'] / (df['QUANT.'].sum() / 100)
    quantity_proportion = round(quantity_proportion, 2)
    return quantity_proportion


def calculate_payed_total(df):
    payed_total = (df['QUANT.'] * df['$ COMPRA'])
    payed_total = round(payed_total, 2)
    return payed_total


def calculate_current_total(df):
    current_total = (df['QUANT.'] * df['$ DIA'])
    current_total = round(current_total, 2)
    return current_total


def calculate_profit(df):
    profit = (df['$ DIA'] * df['QUANT.']) - df['TOTAL PAGO']
    profit = round(profit, 2)
    return profit


def calculate_price_var(df):
    var = (((df['$ DIA'] / df['$ COMPRA']) - 1) * 100)
    var = round(var, 2)
    return var


def var_chart(df):

    empty = '░'
    full = '▇'
    over = '☄'

    scale = 6
    var_list = [i / scale for i in df['VAR']]
    chart_list = []
    for item in var_list:
        item = int(item)
        max_value = int(100 / scale)

        if item >= 0:

            if item > max_value:
                bar = ((empty * max_value) + (full * (max_value - 1)) + over)
                chart_list.append(bar)

            else:
                bar = ((empty * max_value) + (full * item) + (empty * (max_value - item)))
                chart_list.append(bar)

        elif item < 0:
            item_format = max_value - abs(item)
            item_format = int(round(item_format, 0))
            bar = (empty * item_format) + (full * abs(item)) + (empty * max_value)
            chart_list.append(bar)
    return chart_list


def generate_totals(sum_profit_list):
    df = pd.read_csv('./tables/tabela.csv')
    profiles = len(list(df['CARTEIRA'].unique()))
    quantity = len(list(df['SIGLA'].unique()))
    shares = df['QUANT.'].sum()
    sum_total_investido = (df['$ COMPRA'] * df['QUANT.']).sum()
    profit = sum_profit_list[0] + sum_profit_list[1]
    profit = round(profit, 2)

    print('\n')
    print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
    print(f'TOTAL')
    print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
    print('\n')
    print(f'»»» RESUMO:')
    print(f'»»» {profiles} carteiras')
    print(f'»»» {quantity} ações diferentes')
    print(f'»»» {shares} total de ações')
    print(f'»»» {round(sum_total_investido, 2)} reais investidos')
    print(f'»»» {profit} reais de saldo')

# OTHER FUNCTIONS


def stand_by_main():

    print('\n')
    val = input("Tecle 1 para atualizar, 2 para vender ações ou M para voltar ao menu principal.").lower()
    if val == '1':
        portfolio_manager()
    elif val == '2':
        sale_function()
    else:
        pass

# MAIN FUNCTION


def portfolio_manager():
    os.system("clear")
    print("Buscando preço das suas ações...")

    sum_profit_list = []
    portfolio_dict = search_portfolio_list()
    for key in portfolio_dict:
        df = portfolio_dict[key]

        # Run functions and generate columns
        price_list = get_price_list(df)
        df['$ DIA'] = price_list

        quantity_proportion = calculate_proportions(df)
        df['PORC.'] = quantity_proportion

        payed_total = calculate_payed_total(df)
        df['TOTAL PAGO'] = payed_total

        current_total = calculate_current_total(df)
        df['TOTAL ATUAL'] = current_total

        profit = calculate_profit(df)
        df['SALDO'] = profit

        var = calculate_price_var(df)
        df['VAR'] = var

        chart = var_chart(df)
        df[' '] = chart

        # Generate additional data

        sum_profit = df['SALDO'].sum()
        sum_profit_list.append(sum_profit)
        sum_total_investido = df['TOTAL PAGO'].sum()
        stocks_quantity = len(df['SIGLA'].value_counts())
        quantity = df['QUANT.'].sum()

        # Print results
        print('\n')
        print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
              f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
              f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
        print(f'BOLETIM DA CARTEIRA {key.upper()}')
        print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
              f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
              f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
        print('\n')
        print(f'»»» RESUMO:')
        print(f'»»» {stocks_quantity} ações diferentes')
        print(f'»»» {quantity} total de ações')
        print(f'»»» {round(sum_total_investido, 2)} reais investidos')
        print(f'»»» {round(sum_profit, 2)} reais de saldo')
        print('\n')
        print(df[['SIGLA',
                  'DESCRIÇÃO',
                  'DATA',
                  'QUANT.',
                  'PORC.',
                  '$ COMPRA',
                  '$ DIA',
                  'VAR',
                  'TOTAL PAGO',
                  'TOTAL ATUAL',
                  'SALDO',
                  ' ']])
        print('\n')

    generate_totals(sum_profit_list)

    print('\n')
    print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
          f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
    print(f'Atualizado em: {datetime.datetime.now()}')
    print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
            f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
            f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')

    stand_by_main()
