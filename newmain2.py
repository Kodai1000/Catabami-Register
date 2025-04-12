import tkinter as tk
from tkinter import ttk

#商品クラス
class Product:
    def __init__(self, name, price, category, quantity):
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity
    def sum_price(self):
        return self.price*self.quantity

#商品データベースクラス    
class ProductDatabase:
    def __init__(self):
        self.products = []
    def add(self, name, price, cateogy):
        self.products.append(Product(name, price, 0, 1))
    def get(self, i):
        return self.products[i]
    
#テーブルクラス
class Table:
    def __init__(self, name):
        self.name = name
        self.products = []
    def buy(self, bought_product_class, quantity):
        bought_product_class.quantity = quantity
        if bought_product_class in self.products:
            index = self.products.index(bought_product_class)
            self.products[index].quantity += quantity
        else:
            self.products.append(
                bought_product_class
            )
    def sum_price(self):
        sum = 0
        for product in self.products:
            sum += product.sum_price()
        return sum
    def search_products(self, name):
        for i, product in enumerate(self.products):
            if product.name == name:
                return i
        return -1

#テーブル管理
class TablesManager:
    def __init__(self):
        self.tables = []
    def add(self, name):
        self.tables.append(
            Table(name)
        )
    def get(self, i):
        return self.tables[i]
    def get_name_list(self):
        returned = []
        for table in self.tables:
            returned.append(
                table.name
            )
        return returned
    
#UI
class ui:
    def __init__(self, root, productdatabase, tablesmanager):
        self.root = root
        self.pdb = productdatabase
        self.tm = tablesmanager
        self.Table_Area_Init()
        self.root.mainloop()
        self.Selected_Table_Combo = -1

    def Table_Combo_On_Selected(self, event=None):
        self.Selected_Table_Combo = self.Table_Combo.get()
        self.Table_Data_Set(self.Selected_Table_Combo)
        return self.Selected_Table_Combo

    def Table_Area_Init(self):
        self.Table_Area_Frame = tk.Frame(self.root)

        self.Table_Combo = ttk.Combobox(self.root, values=self.tm.get_name_list())
        self.Table_Combo.pack(pady=10)
        self.Table_Combo.bind('<<ComboboxSelected>>', self.Table_Combo_On_Selected)

        self.Table_Area_Frame.pack()

    def Table_Data_Set(self, table_name):
        self.Table_Area_Frame.destroy()
        self.Table_Area_Frame = tk.Frame(self.root)
        self.Table_Area_Frame.pack()
        for table in self.tm.tables:
            if table.name == table_name:
                table_products = table.products
                break
        else:
            return  # 該当なし
        for product in table.products:
            self.Add_to_table_obj(product)

        
    
    def Add_to_table_obj(self, table_product):
        
        product_frame = tk.Frame(self.Table_Area_Frame)
        product_frame.pack()
        label_name = tk.Label(product_frame, text=table_product.name)
        label_name.grid(row=0, column=0)

        label_unitprice = tk.Label(product_frame, text=table_product.price)
        label_unitprice.grid(row=0, column=1)

        button_minus = tk.Button(product_frame, text="-")
        button_minus.grid(row=0, column=2)

        label_quantitiy = tk.Label(product_frame, text=table_product.quantity)
        label_quantitiy.grid(row=0, column=3)

        button_plus = tk.Button(product_frame, text="+")
        button_plus.grid(row=0, column=4)

        label_sumprice = tk.Label(product_frame, text=table_product.sum_price())
        label_sumprice.grid(row=0, column=5)
        
    def update(self):
        label_name = 

if __name__ == "__main__":
    ProductDatabase = ProductDatabase()
    TablesManager = TablesManager()
    
    ProductDatabase.add("cake", 100, 0)
    ProductDatabase.add("coffee", 100, 0)

    root = tk.Tk()
    root.geometry("800x800")
    
    TablesManager.add("東郷")
    TablesManager.add("松浦")

    TablesManager.tables[0].buy(ProductDatabase.products[0], 1)
    TablesManager.tables[1].buy(ProductDatabase.products[1], 1)

    ui(root, ProductDatabase, TablesManager)