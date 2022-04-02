import csv


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


def get_sales_data(data):
    """
    get sales figures from the user
    """
    
    sales = []
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

sales = get_sales_data(items)
print(sales[0].item)
