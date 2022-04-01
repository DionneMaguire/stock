class Sales:
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
    print("Please enter sales figures for the following items:")
    data_str1 = input("Enter sales figures for coke here:")
    print(f'The data provided is {data_str1}')
    sales_1 = Sales('coke', data_str1, False)
    sales = []
    sales.append(sales_1)
    print(sales_1._str_())

get_sales_data()