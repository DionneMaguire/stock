import csv


def get_figures_from_csv(file_name):
    """
    read csv file into a dictionary
    """
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        results = []

        for row in csv_reader:
            results.append(dict(row))

        return results

         
class Sales():
    """
    creates an instance of Sales
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


def get_sales_data(data):
    """
    get sales figures from the user.
    check numbers entered are positive numbers by
    checking in get_non_negative_int function
    Save the sales figures in a list called sales
    """
    sales = []
    print("Please enter sales figures for the following items: ")
    
    for x in data:

        data_str = get_non_negative_int(f"Enter sales figures for {x} here:\n")

        print(f'The sales data provided for {x} is {data_str}')
        salesx = Sales(x, data_str, False)
    
        sales.append(salesx)
        print(salesx._str_())

    return sales


def update_sales_csv(data):
    """
    Write sales figures to a sales.csv file
    """
    headings = ['item', 'quantity', 'is_audited']

    with open('csvfiles/sales.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headings)

        for data in data:
            writer.writerow([data.item, data.quantity, data.is_audited])
        
    print("sales file successfully updated!")    


def update_stocks(stock_data, sales_data):
    """
    gets the stock value for each item and takes away the sales 
    figure inputted by the user to give the current stock value
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
                print(f"For {i['item']} updated stock is {stock_updated}")
                i['quantity'] = stock_updated
                if stock_updated < int(i['reorder_level']):
                    print(f"Reorder {i['item']}, only have {stock_updated}")
                    reorder = (i['item'], stock_updated)
                    reorder_file.append(reorder)
                else:
                    continue
    print("updated stock quantity")
    return reorder_file


def update_stock_csv(data):
    """
    Write updated stock figures to a stock.csv file
    """
    headings = ['item', 'quantity', 'reorder_level']

    with open('csvfiles/stock.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headings)
        writer.writeheader()

#        for data in data:
        writer.writerows(data)
        
    print("stock file successfully updated!") 


def main(): 
    """
    Main function 
    """
    stocks = get_figures_from_csv('csvfiles/stock.csv')
    print(stocks)
    items = ['coke', 'fanta', 'water']

    sales = get_sales_data(items)

    update_sales_csv(sales)
    sales_dict = get_figures_from_csv('csvfiles/sales.csv')

    reorder_data = update_stocks(stocks, sales_dict)
    print(stocks)
    print(reorder_data)
    update_stock_csv(stocks)
#    update_reorder_csv(reorder_data)

main()