from tabulate import tabulate

data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

print(tabulate(data, headers='firstrow', showindex='always',tablefmt='fancy_grid'))  

data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

print(tabulate(data, headers='firstrow', showindex='always', tablefmt='jira'))


data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

print(tabulate(data, headers='firstrow', showindex='always',    

           tablefmt='plain'))


data = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]

print(tabulate(data, headers='firstrow', showindex='always', 

         tablefmt='textile'))