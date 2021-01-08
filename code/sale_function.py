import pandas as pd
import datetime


def sale_function():
    print('\n')
    stock_index = input("Qual o index da ação que você deseja vender? (Pressione M para voltar ao menu.)").lower()

    if stock_index == 'm':
        pass

    else:
        df = pd.read_csv('./tables/tabela.csv')
        try:
            stock_index = int(stock_index)
            if stock_index > len(df):
                print('Ops, não encontramos o índice desta ação. Tente novamente.')
                sale_function()
            else:
                price = input('Qual é o preço da venda?')
                price = int(price)
                stock_series = df.loc[stock_index]
                profit = (price - stock_series['$ COMPRA']) * stock_series['QUANT.']
                profit = round(profit, 2)

                print('\n')
                print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
                print(f'BOLETIM DE VENDA')
                print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
                print(stock_series)
                print(f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»'
                      f'»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»')
                print('\n')
                confirm = input(f'Você deseja vender as ações acima por {price} reais cada unidade? '
                                f'Você terá um lucro de {profit} reais. '
                                f'(s/n) ')
                if confirm == 'n':
                    print('Tudo bem. Tente novamente.')
                    pass
                elif confirm == 's':  # Main option
                    organize_table(stock_index, stock_series, price, profit)
                    pass
                else:
                    sale_function()

                sale_function()

        except Exception as e:
            print('Algo deu errado. Tente novamente.')
            sale_function()


def organize_table(stock_index, stock_series, price, profit):
    date_today = datetime.date.today()
    date_today = f'{date_today.day}-{date_today.month}-{date_today.year}'

    df_history = pd.read_csv('./tables/historico.csv')
    df = pd.DataFrame({'SIGLA': stock_series['SIGLA'],
                       'DESCRIÇÃO': stock_series['DESCRIÇÃO'],
                       'QUANT.': stock_series['QUANT.'],
                       'DATA COMPRA': stock_series['DATA'],
                       'DATA VENDA': date_today,
                       '$ COMPRA': stock_series['$ COMPRA'],
                       '$ VENDA': price,
                       'SALDO': [profit]})
    df_history = pd.concat([df_history, df], ignore_index=True)
    df_history.to_csv('./tables/historico.csv', index=False)

    df_tabela = pd.read_csv('./tables/tabela.csv')
    df_tabela = df_tabela.drop(stock_index)
    df_tabela.to_csv('./tables/tabela.csv', index=False)

    print('Vendido!')
    print('\n')
    sale_again()


def sale_again():
    again = input('Deseja vender mais ações? (s/n)')
    if again == 's':
        sale_function()
    elif again == 'n':
        pass
    else:
        sale_again()
