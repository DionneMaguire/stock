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

def get_sales_data():
    """
    get sales figures from the user
    """
    items = ['coke','fanta','water']
    sales =[]
    print("Please enter sales figures for the following items: ")
    
    for x in items:

        data_str = input(f"Enter sales figures for {x} here:")
        print(f'The data provided for {x} is {data_str}')
        salesx = Sales(x, data_str, False)
    
        sales.append(salesx)
        print(salesx._str_())

    return sales

sales = get_sales_data()
print(sales[0].item)
