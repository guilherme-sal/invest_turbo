import os
from portfolio_manager import portfolio_manager
from get_stock_description import get_stock_description
from transaction_archive import show_history

def main_function():
    os.system('clear')
    os.system('cat ./banner/menu.txt')
    value = input("").lower()
    if value == '1':
        portfolio_manager()
        main_function()
    elif value == '2':
        show_history()
        main_function()
    elif value == '3':
        get_stock_description()
        main_function()
    elif value == 'q':
        pass
    else:
        main_function()


main_function()
