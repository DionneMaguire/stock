import csv

products = ['coke', 'fanta', 'water']
stock_headings = ['item', 'quantity', 'reorder_level']
sales_headings = ['item', 'quantity', 'is_audited']
reorder_headings = ['item', 'current_stock']

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


def write_sales_csv(data, headings):
    """
    Write data from a list to a csv file
    """
    

    with open('csvfiles/sales.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headings)

        for data in data:
            writer.writerow([data.item, data.quantity, data.is_audited])
      
    print("sales file successfully updated!")  


def update_stocks(stock_data, sales_data):
    """
    gets the stock value for each item and takes away the sales
    figure inputted by the user to give the current stock quantity
    and update the quantity in stock dictionary.
    Then check if the updated stock value is below the reorder
    level and if it is write the item and the current stock to
    reorder_file.
    """
    reorder_file = []
    for i in stock_data:
        for j in sales_data:
            if i['item'] == j['item']:
                stock_updated = int(i['quantity']) - int(j['quantity'])
                i['quantity'] = stock_updated
                if stock_updated < int(i['reorder_level']):
                    reorder = {'item': i['item'], 'current_stock': stock_updated}
                    reorder_file.append(reorder)
                else:
                    continue

    print("updated stock quantity")
    return reorder_file


def write_csv_file(data, headings, file):
    """
    Write data to a csv file
    """
    with open(file, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headings)
        writer.writeheader()

        writer.writerows(data)     


def reorder_print(data):
    """
    Check if there are items for reorder and if not print
    message to user.
    """
    if data == []:
        print("------------------------------")
        print("Nothing needs to be reordered!")
        print("------------------------------")
    else:
        print("--------------------------------")
        print("Items that need to be reordered:")
        print("--------------------------------")
        format_figures(data, 'reorder')


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

    reorder_data = update_stocks(stocks, sales)
    reorder_print(reorder_data)

    write_csv_file(stocks, stock_headings, 'csvfiles/stock.csv')

    write_csv_file(reorder_data, reorder_headings, 'csvfiles/reorder.csv')


print("Welcome to Stock Program!")
print("-------------------------\n")
main()
