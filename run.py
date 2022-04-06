import csv


def get_stock_figures():
    """
    read stock csv file into a dictionary
    """

    with open('csvfiles/stock.csv', mode='r') as csv_file:
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
    while True:
        try:
            value = int(input(prompt))
            print(value)
        except ValueError:
            print("Sorry, I didn't understand that.")
            continue
        if value < 0:
            print("sorry, your response must not be negative.")
            continue
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

        data_str = get_non_negative_int(f"Enter sales figures for {x} here:")
        print(data_str)

        print(f'The data provided for {x} is {data_str}')
        salesx = Sales(x, data_str, False)
    
        sales.append(salesx)
        print(salesx._str_())

    return sales

def update_sales_csv(data, items):
    """
    Write sales figures to a sales.csv file
    """
    headings = ['item','quantity','is_audited']

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
    and write this back to the stock quantity in csv file
    """
#    products = [d['item'] for d in stock_data]
#    quantities = [d['quantity'] for d in stock_data]
#    print(products)
#    print(quantities)
    for i in stock_data:
        for j in sales_data:
            print(stock_data[i].get('item'))
            print(sales_data[j].get('item'))
            if stock_data[i].get('item') == sales_data[j].get('item'):
                updated_stock = int(stock_data[i].get('quantity')) - int(sales_data[j].get('quantity'))
                print(updated_stock)
                
                 

        


    
stocks = get_stock_figures()
print(stocks)
items = ['coke','fanta','water']

sales = get_sales_data(items)
print(sales)

update_sales_csv(sales, items)

#update_stocks(stocks, sales)