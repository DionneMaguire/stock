import os
from datetime import datetime
import csv


products = ['coke', 'fanta', 'water']
stock_headings = ['item', 'quantity', 'reorder_level']
sales_headings = ['item', 'quantity', 'is_audited']
reorder_headings = ['item', 'current_stock']


class Stock():
    def __init__(self, item, quantity, reorder_level):
        self.item = item
        self.quantity = quantity
        self.reorder_level = reorder_level


def user_input_stock():
    """
    user enters stock - item, quantity and reorder_level
    check quantity and reorder_level are numbers and zero or greater
    """
    enter_new_stock = True
    stocks = []
    while enter_new_stock:
        item = input("Enter name of product\n")
        quantity = get_non_negative_int(
            f"Enter current quantity of {item} in stock\n")
        reorder_level = get_non_negative_int(
            f"What quantity of {item} is reorder level\n")
        stocks.append(Stock(item, quantity, reorder_level).__dict__)
        enter_new_stock = input(
            "Do you want to enter a new stock, enter yes\n") == "yes"

    print(stocks)
    return stocks


def read_csv(file_name):
    """
    read csv file into a dictionary
    """
    with open(file_name, mode='r') as csv_file:
        return list(csv.DictReader(csv_file))


def format_figures(data, type):
    """
    format data to make it easier to read for user
    """
    for i in data:
        if type == 'stock':
            print(f"{i['item']} stock available is: {i['quantity']}")
        elif type == 'reorder':
            print(f"{i['item']} current stock is {i['current_stock']}")


class Sales():
    """
    creates an instance of Sales class for a product
    """
    def __init__(self, item, quantity, is_audited):
        self.item = item
        self.quantity = quantity
        self.is_audited = is_audited

    def _str_(self):
        return f'{self.item} {self.quantity}'


def get_non_negative_int(prompt):
    """
    checks that the user input is a number 0 or greater
    and not greater than 40 (initial stock)
    """
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, your response must be a number")
            continue
        if value < 0:
            print("sorry, your response must not be negative.")
            continue
        elif value > 40:
            print("Sorry, your response must not be greater than 40")
        else:
            break
    return value


def get_sales():
    """
    get sales figures from the user.
    check numbers entered are positive numbers by
    checking in get_non_negative_int function
    Save the sales figures in a list called sales
    """
    sales = []

    for product in products:
        quantity = get_non_negative_int(f"How much {product} did you sell?\n")
        print(f'Sales of {quantity} of {product} has been recorded.') 
        sales.append(Sales(product, quantity, False).__dict__)
    return sales


def update_stocks(stocks, sales):
    """
    gets the stock quantity and takes away the sales to get current
    stock and update quantity.
    check if quantity now is below reorder level and if it is
    write to reorder list.
    """
    reorder_list = []
    _stocks = stocks
    _sales = sales
    for stock in _stocks:
        for sale in _sales:
            if stock['item'] == sale['item']:
                stock_updated = int(stock['quantity']) - int(sale['quantity'])
                stock['quantity'] = stock_updated
                sale['is_audited'] = True
                if stock_updated < int(stock['reorder_level']):
                    reorder = {'item': stock['item'], 
                               'current_stock': stock_updated}
                    reorder_list.append(reorder)
                else:
                    continue

    print("updated stock quantity")
    return reorder_list, _stocks, _sales


def write_csv_file(figures, headings, file):
    """
    Write data to a csv file
    """
    with open(file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headings)
        writer.writeheader()

        writer.writerows(figures)   


def reorder_print(list):
    """
    Check if there are items for reorder and if not print
    message to user.
    """
    if list == []:
        print("------------------------------")
        print("Nothing needs to be reordered!")
        print("------------------------------")
    else:
        print("--------------------------------")
        print("Items that need to be reordered:")
        print("--------------------------------")
        format_figures(list, 'reorder')


def main():
    """
    Main function
    Need to set initial stock in csv file
    """
    initial_stock = [
        {'item': 'coke', 'quantity': '40', 'reorder_level': '20'},
        {'item': 'fanta', 'quantity': '40', 'reorder_level': '20'},
        {'item': 'water', 'quantity': '40', 'reorder_level': '20'}
        ]
  
    write_csv_file(initial_stock, stock_headings, 'csvfiles/stock.csv')

    stocks = read_csv('csvfiles/stock.csv')
    format_figures(stocks, 'stock')

    sales = get_sales()
    write_csv_file(sales, sales_headings, 'csvfiles/sales.csv')

    reorder_list, new_stocks, updated_sales = update_stocks(stocks, sales)
    write_csv_file(updated_sales, sales_headings, 'csvfiles/sales.csv') 
    write_csv_file(new_stocks, stock_headings, 'csvfiles/stock.csv')

    reorder_print(reorder_list)
    reorder_file_name = (
        f'csvfiles/reorders/{datetime.now().strftime("%m_%d_%y_%H:%M")}.csv')
    write_csv_file(reorder_list, reorder_headings, reorder_file_name)

    print(f"You can also find your reorder list here {os.getcwd()}/{reorder_file_name}")


if __name__ == "__main__":
    print("Welcome to Stock Program!")
    print("-------------------------\n")
    main()
#    input_stock = user_input_stock()
#    write_csv_file(input_stock, stock_headings, 'csvfiles/stock.csv')
