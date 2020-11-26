from tabulate import tabulate

data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

print(tabulate(data, headers='firstrow', showindex='always',tablefmt='fancy_grid'))  

data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

# print(tabulate(data, headers='firstrow', showindex='always', tablefmt='jira'))


# data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

# print(tabulate(data, headers='firstrow', showindex='always',    

#            tablefmt='plain'))


# data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

# print(tabulate(data, headers='firstrow', showindex='always', 

#          tablefmt='textile'))

def write_cols(data):
    col_spacer = "   "      # added between columns
    widths = [0] * len(data[0])

    # Calculate the widest entry for each column
    for row in data:
        widths[:] = [max(widths[index], len(str(col))) for index, col in enumerate(row)]

    return [col_spacer.join("{:<{width}}".format(col, width=widths[index]) for index, col in enumerate(row)) for row in data]

data = [['', 'Config 1', '', 'Config 2', ''], ["Test", "Data 1", "Data 2", "Data 1", "Data 2"], ["abc", "123", "123", "123", "123"]]

for row in write_cols(data):
    print (row)