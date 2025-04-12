#Business Logic
# 商品情報(class ProductsInformation)
# レシートデータ管理(class ReceiptData)
# 
import tkinter as tk
from tkinter import ttk

class ProductsInformation:
    def __init__(self):
        self.products = []
        self.categories = [
            "food",
            "drink"
        ]

    def add(self, name, price, category):
        self.products.append(
            {
                "name":name,
                "price":price,
                "category":category
            }
        )

class Receipt:
    def __init__(self, products_information):
        self.tables = []
        self.products_information = products_information
        
    def add_table(self, name):
        self.tables.append({
            "name":name,
            "products_list":[]
        })
    
    def add_product_to_table(self, table_id, product_id,quantity):
        bought = self.products_information.products[product_id]
        print(table_id, self.tables)
        self.tables[table_id]["products_list"].append(
            {
                "name":bought["name"],
                "price":bought["price"],
                "quantity":quantity
            }
        )
    
    def plus_quantity(self, table_id, products_list_id):
        self.tables[table_id][products_list_id]["quantity"] += 1

    def minus_quantity(self, table_id, products_list_id):
        self.tables[table_id][products_list_id]["quantity"] -= 1

    def destroy_product_from_receipt(self, table_id, products_list_id):
        del self.tables[table_id][products_list_id]

    
class UI:
    def __init__(self, root, receipt, products_information):
        self.root = root
        self.receipt = receipt
        self.products_information = products_information
        
        self.receipt_tab_init()
        self.products_tab_init()
        
    def receipt_tab_init(self):
        self.receipt_tab_control = ttk.Notebook()
        self.receipt_tab = []
        self.tables_objs = []
        self.receipt_tab_control.pack()

    def add_table(self, name):
        frame = tk.Frame(self.receipt_tab_control)
        self.receipt_tab_control.add(frame, text=name)
        self.receipt_tab.append(frame)
        self.receipt.add_table(name)

    def products_tab_init(self):
        self.products_tab_control = ttk.Notebook()
        self.products_tabs = []
        for i, category in enumerate(products_information.categories):
            frame = tk.Frame(self.products_tab_control)
            self.products_tab_control.add(frame, text=category)
            self.products_tabs.append(frame)
        self.products_tab_control.pack()

        for i, product in enumerate(products_information.products):
            category = product["category"]
            button = tk.Button(self.products_tabs[category], text=product["name"] + " " + str(product["price"]), command = lambda i=i:self.add_product_to_table(i,1))
            button.pack()

    def add_product_to_table(self, product_id, quantity):
        table_id  = self.receipt_tab_control.index("current")
        bought = self.products_information.products[product_id]
        frame = tk.Frame(self.receipt_tab[table_id])
        label_name = tk.Label(frame, text=bought["name"])
        label_unitprice = tk.Label(frame, text=bought["price"])
        minus_button = tk.Button(frame, text="-")
        label_quantity = tk.Label(frame, text=quantity)
        plus_button =tk.Button(frame, text="+")
        label_sumprice = tk.Label(frame, text=bought["price"]*quantity)
        label_name.grid(row=0, column=0)
        label_unitprice.grid(row=0,column=1)
        minus_button.grid(row=0, column=3)
        label_quantity.grid(row=0, column=4)
        plus_button.grid(row=0, column=5)
        label_sumprice.grid(row=0, column=6)
        frame.pack()
        self.tables_objs.append(
            {
                "frame":frame,
                "label_name":label_name,
                "label_unitprice":label_unitprice,
                "minus_button":minus_button,
                "label_quantitiy":label_quantity,
                "plus_button":plus_button,
                "label_sumprice":label_sumprice
            }
        )
        self.receipt.add_product_to_table(table_id, product_id, quantity)



if __name__ == "__main__":
    products_information = ProductsInformation()

    products_information.add("Cake", 100, 0)
    products_information.add("Beer",200, 1)

    receipt = Receipt(products_information)

    
    root = tk.Tk()
    root.geometry("800x800")

    ui = UI(root, receipt, products_information)
    
    ui.add_table("Customer 1")
    ui.add_product_to_table(0,1)

    root.mainloop()