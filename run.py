import os
from datetime import datetime
import csv


stock_headings = ['item', 'quantity', 'reorder_level']
sales_headings = ['item', 'quantity', 'is_audited']
reorder_headings = ['item', 'current_stock']


class Stock():
    """
    creates an instance of stock class for a product
    """
    def __init__(self, item, quantity, reorder_level):
        self.item = item
        self.quantity = quantity
        self.reorder_level = reorder_level


def user_input_stock():
    """
    user enters stock - item, quantity and reorder_level
    check quantity and reorder_level are numbers and zero or greater
    """
    print("Let's get your stock ready!")
    enter_new_stock = True
    stocks = []
    while enter_new_stock:
        item = input("Enter name of product\n")
        quantity = get_non_negative_int(
            f"Enter current quantity of {item} in stock\n", None)
        reorder_level = get_non_negative_int(
            f"What quantity of {item} is reorder level?\n", None)
        stocks.append(Stock(item, quantity, reorder_level).__dict__)
        enter_new_stock = input(
            "Do you want to enter a new product? enter yes\n") == "yes"

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


def get_list_products(stocks):
    """
    get a list of products from stock
    """
    products = []
    for stock in stocks:
        products.append(stock['item'])
    return products


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


def get_non_negative_int(prompt, stock_level):
    """
    checks that the user input is a number 0 or greater
    and not greater than stock quantity of product
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
        elif (stock_level is not None) and (value > stock_level):
            print(
                f"Sorry, your response must not be greater than {stock_level}")
        else:
            break
    return value


def get_sales(products, stocks):
    """
    get sales figures from the user.
    check numbers entered are positive numbers by
    checking in get_non_negative_int function
    Save the sales figures in a list called sales
    """
    sales = []

    for product in products:
        for stock in stocks:
            if stock['item'] == product:
                max_quantity = int(stock['quantity'])
                quantity = get_non_negative_int(
                   f"What quantity of {product} did you sell?\n", max_quantity)
                print(f'Sales of {quantity} of {product} has been recorded.')
                sales.append(Sales(product, quantity, False).__dict__)
    return sales


def update_stocks(stocks, sales):
    """
    get the stock quantity and take away the sales to get current
    stock and update quantity in stock.
    update is_audited in sales
    check if quantity now is below reorder level and if it is
    write to reorder list.
    return reorder list, updated stocks and updated sales
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

    return reorder_list, _stocks, _sales


def write_csv_file(figures, headings, file):
    """
    Write data to a csv file
    """
    with open(file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headings)
        writer.writeheader()

        writer.writerows(figures)


def reorder_print(list, reorder_file_name):
    """
    Check if there are items for reorder and print
    them to the console and if not print
    message to user that nothing needs reordered
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
        print("You can also find your reorder list here:")
        print(f"{os.getcwd()}/{reorder_file_name}")


def main():
    """
    Main function
    """
    input_stock = user_input_stock()
    write_csv_file(input_stock, stock_headings, 'csvfiles/stock.csv')

    stocks = read_csv('csvfiles/stock.csv')
    format_figures(stocks, 'stock')
    products = get_list_products(stocks)

    sales = get_sales(products, stocks)
    write_csv_file(sales, sales_headings, 'csvfiles/sales.csv')

    reorder_list, new_stocks, updated_sales = update_stocks(stocks, sales)
    write_csv_file(updated_sales, sales_headings, 'csvfiles/sales.csv')
    write_csv_file(new_stocks, stock_headings, 'csvfiles/stock.csv')

    reorder_file_name = (
        f'csvfiles/reorders/{datetime.now().strftime("%m_%d_%y_%H:%M")}.csv')
    write_csv_file(reorder_list, reorder_headings, reorder_file_name)
    reorder_print(reorder_list, reorder_file_name)


if __name__ == "__main__":
    print("Welcome to Stock Program!")
    print("-------------------------\n")
    main()
