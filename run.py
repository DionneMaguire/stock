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

class Stock():
    """
    creates an instance of stock
    """
    def __init__(self, item, stock_quantity, reorder_level):
        self.item = item
        self.stock_quantity = stock_quantity
        self.reorder_level = reorder_level
    def _str_(self):
        return f'{self.item} {self.stock_quantity} {self.reorder_level}'

def create_stock_records(data):
    """
    creates stock instances for all items
    """

    stocks = []

    for x in data:
        stocksx = Stock(x,40,20)
        stocks.append(stocksx)
        print(stocksx._str_())

    return stocks

def get_sales_data(data):
    """
    get sales figures from the user
    """
    
    sales =[]
    print("Please enter sales figures for the following items: ")
    
    for x in data:

        data_str = input(f"Enter sales figures for {x} here:")
        print(f'The data provided for {x} is {data_str}')
        salesx = Sales(x, data_str, False)
    
        sales.append(salesx)
        print(salesx._str_())

    return sales

def update_stocks():
    """
    gets the stock value for each item and takes away the sales 
    figure inputted by the user to give the current stock value
    and write this back to the stock quantity in class
    """
    

items = ['coke','fanta','water']
stocks = create_stock_records(items)
print(stocks[1].reorder_level)
sales = get_sales_data(items)
print(sales[0].item)
