import tkinter as tk
from tkinter import ttk

# 商品リスト（商品名と価格）
products = [
    {"name": "りんご", "price": 100, "category":0},
    {"name": "コーヒー", "price": 50, "category":1},
    {"name": "Orange", "price": 80, "category":0},
    {"name": "ジュース", "price": 150, "category":1},
]
categories = [
    "食品",
    "ドリンク",
]
categories_colors = [
    "LightPink1",
    "light sky blue"
]

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("レジ")


        self.tab_init()
        self.product_buttons_set()


    def tab_init(self):
        self.tab_control = ttk.Notebook(root)
        self.tabs = [
            {
                "frame":tk.Frame(self.tab_control),
                "name":"テーブル1",
            },
            {
                "frame":tk.Frame(self.tab_control),
                "name":"テーブル2"
            },
        ]
        self.productsOBJs_in_tab = [[], []]
        self.tabsOBJs = []
        for i, tab in enumerate(self.tabs):
            self.tab_control.add(tab["frame"], text = tab["name"])
            self.tabsOBJs.append(
                {
                    "title":tk.Label(tab["frame"], text = str(tab["name"])),
                }
            )
            self.tabsOBJs[-1]["SumLettersLabel"] = tk.Label(tab["frame"], text="SUM", width=10, anchor="e", font=("Courier", 12))
            self.tabsOBJs[-1]["sum"] = tk.Label(tab["frame"], text="0", width=10, anchor="e", font=("Courier", 12))

            self.tabsOBJs[-1]["title"].grid(row=0, column=0, columnspan=6, sticky="w", pady=(5, 10))
            self.tabsOBJs[-1]["SumLettersLabel"].grid(row=999, column=4, sticky="e")
            self.tabsOBJs[-1]["sum"].grid(row=999, column=5, sticky="e")
        self.tab_control.pack(expand=True, fill="both")
        self.add_product_to_tab(0)
        self.add_product_to_tab(1)
        self.add_product_to_tab(2)
        self.add_product_to_tab(3)

    
    def calculate_and_print_sum(self, tab_number):
        sum = 0
        for productOBJ in self.productsOBJs_in_tab[tab_number]:
            sum += int(productOBJ["quantity"]["text"]) * int(productOBJ["unit_price"]["text"])
        print(self.tabsOBJs)
        self.tabsOBJs[tab_number]["sum"]["text"] = str(sum)     

    def add_product_to_tab(self, prodcut_number):
        bg_color = categories_colors[products[prodcut_number]["category"]]
        index = self.tab_control.index("current")
        id = len(self.productsOBJs_in_tab[index])
        print("index", index)
        self.productsOBJs_in_tab[index].append(
            {
                "frame":tk.Frame(self.tabs[index]["frame"], bg=bg_color),
            }
        )
        self.productsOBJs_in_tab[index][-1]["label"] = tk.Label(
            self.productsOBJs_in_tab[index][-1]["frame"], 
            text = products[prodcut_number]["name"],
            width=10,  # 固定幅を設定
            anchor="e",  # 右寄せ
            font=("Courier", 12),  # 等幅フォント
            bg=bg_color
        )
        self.productsOBJs_in_tab[index][-1]["unit_price"] = tk.Label(
            self.productsOBJs_in_tab[index][-1]["frame"], 
            text = str(products[prodcut_number]["price"]),
            width=10,  # 固定幅を設定
            anchor="e",  # 右寄せ
            font=("Courier", 12),  # 等幅フォント
            bg=bg_color
        )
        self.productsOBJs_in_tab[index][-1]["minus_button"] = tk.Button(
            self.productsOBJs_in_tab[index][-1]["frame"], 
            text = "-",
            command = lambda:self.minus_product_in_tab(id)
        )
        self.productsOBJs_in_tab[index][-1]["quantity"] = tk.Label(
            self.productsOBJs_in_tab[index][-1]["frame"], 
            text = 1,
            width=1,  # 固定幅を設定
            anchor="e",  # 右寄せ
            font=("Courier", 12),  # 等幅フォント
            bg=bg_color
        )
        self.productsOBJs_in_tab[index][-1]["plus_button"] = tk.Button(
            self.productsOBJs_in_tab[index][-1]["frame"], 
            text = "+",
            command = lambda:self.plus_product_in_tab(id)
        )
        self.productsOBJs_in_tab[index][-1]["sum"] = tk.Label(
            self.productsOBJs_in_tab[index][-1]["frame"],
            width=10,  # 固定幅を設定
            anchor="e",  # 右寄せ
            font=("Courier", 12),  # 等幅フォント
            text = str(products[prodcut_number]["price"]),
            bg=bg_color
        )

        self.productsOBJs_in_tab[index][-1]["frame"].grid(row=id, column=0, columnspan=6, sticky="w")
        self.productsOBJs_in_tab[index][-1]["label"].grid(row=0,column=0)
        self.productsOBJs_in_tab[index][-1]["unit_price"].grid(row=0,column=1)
        self.productsOBJs_in_tab[index][-1]["minus_button"].grid(row=0,column=2)
        self.productsOBJs_in_tab[index][-1]["quantity"].grid(row=0,column=3)
        self.productsOBJs_in_tab[index][-1]["plus_button"].grid(row=0,column=4)
        self.productsOBJs_in_tab[index][-1]["sum"].grid(row=0,column=5)
        
        self.calculate_and_print_sum(self.tab_control.index("current"))

    def plus_product_in_tab(self,i):
        print("i", i-1)
        index = self.tab_control.index("current")
        self.productsOBJs_in_tab[index][i]["quantity"]["text"] = str( int(self.productsOBJs_in_tab[index][i]["quantity"]["text"]) + 1 )
        self.productsOBJs_in_tab[index][i]["sum"]["text"] = str( int(self.productsOBJs_in_tab[index][i]["unit_price"]["text"]) * int(self.productsOBJs_in_tab[index][i]["quantity"]["text"]))
        self.calculate_and_print_sum(index)

    def minus_product_in_tab(self,i):
        index = self.tab_control.index("current")
        self.productsOBJs_in_tab[index][i]["quantity"]["text"] = str( int(self.productsOBJs_in_tab[index][i]["quantity"]["text"]) - 1 )
        self.productsOBJs_in_tab[index][i]["sum"]["text"] = str( int(self.productsOBJs_in_tab[index][i]["unit_price"]["text"]) * int(self.productsOBJs_in_tab[index][i]["quantity"]["text"]))

        if int(self.productsOBJs_in_tab[index][i]["quantity"]["text"])<=0:
            self.erase_product_to_tab(i)

        self.calculate_and_print_sum(index)

    def erase_product_to_tab(self, buyed_product_number):
        index = self.tab_control.index("current")
        self.productsOBJs_in_tab[index][buyed_product_number]["label"].destroy()
        self.productsOBJs_in_tab[index][buyed_product_number]["frame"].destroy()
        del self.productsOBJs_in_tab[index][buyed_product_number]
        # ID を更新
        for new_id, productOBJ in enumerate(self.productsOBJs_in_tab[index]):
            productOBJ["minus_button"]["command"] = lambda i=new_id: self.minus_product_in_tab(i)
            productOBJ["plus_button"]["command"] = lambda i=new_id: self.plus_product_in_tab(i)

        self.calculate_and_print_sum(index)
        
    def product_buttons_set(self):
        self.tabs_control_products = ttk.Notebook(root)
        self.tabs_products = []
        for category in categories:
            self.tabs_products.append(
                {
                    "frame":tk.Frame(self.tabs_control_products),
                    "name":category
                }
            )
            self.tabs_control_products.add(self.tabs_products[-1]["frame"], text=str(self.tabs_products[-1]["name"]))

        #self.product_frame = tk.Frame(root)
        #self.product_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.products_buttons = []
        #for products_button in self.products_buttons:
        #    products_button.destroy()
        #self.products_buttons = []
        for i, product in enumerate(products):
            print(i)
            self.products_buttons.append(
                tk.Button(
                    self.tabs_products[product["category"]]["frame"],
                    text=f"{product['name']}\n{product['price']}円",
                    command=lambda i=i:self.add_product_to_tab(i),
                    bg=categories_colors[products[i]["category"]]
                )
            )
            self.products_buttons[-1].pack()
        self.tabs_control_products.pack(expand=True, fill="both")
    
root = tk.Tk()
root.geometry("800x800")
Register = Register(root)
#button = tk.Button(root, text="destroy", command = lambda:Register.erase_product_to_tab(1))
#button.pack()
root.mainloop()