import tkinter as tk
from tkinter import ttk
from datetime import datetime
import json
import os
from PIL import Image, ImageDraw, ImageFont
import datetime
import time


class CategoryDB:
    def __init__(self, path="category_labels.json"):
        with open(path, "r", encoding="utf-8") as f:
            self.categories = json.load(f)

    def get_name(self, category_id: int) -> str:
        return self.categories.get(str(category_id), {}).get("name", f"カテゴリ{category_id}")

    def get_color(self, category_id: int) -> str:
        return self.categories.get(str(category_id), {}).get("color", "#ffffff")


#会計アーカイブ
class ArchivedTransaction:
    def __init__(self, table_name, products):
        self.table_name = table_name
        self.products = products  # コピーする
        self.timestamp = datetime.datetime.now()

    def __str__(self):
        items = ", ".join(f"{p.name}×{p.quantity}" for p in self.products)
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.table_name}: {items}"

#会計アーカイブ管理
class ArchivedManager:
    def __init__(self):
        self.archived = []

    def archive(self, table):
        archived_products = [Product(p.name, p.price, p.category, p.quantity) for p in table.products]
        self.archived.append(ArchivedTransaction(table.name, archived_products))

# 商品クラス
class Product:
    def __init__(self, name, price, category, quantity):
        self.name = name
        self.price = price
        self.category = category
        self.quantity = quantity

    def sum_price(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "quantity": self.quantity
        }


    def from_dict(data):
        return Product(data["name"], data["price"], data["category"], data["quantity"])
    
# 商品データベースクラス
class ProductDatabase:
    def __init__(self):
        self.products = []

    def add(self, name, price, category):
        self.products.append(Product(name, price, category, 1))

    def get(self, i):
        return self.products[i]

    def to_dict(self):
        return [product.to_dict() for product in self.products]

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.products = [Product.from_dict(p) for p in data]
# テーブルクラス
class Table:
    def __init__(self, name):
        self.name = name
        self.products = []

    def buy(self, product_db, product_index, quantity):
        base_product = product_db.get(product_index)
        new_product = Product(base_product.name, base_product.price, base_product.category, quantity)
        index = self.search_products(new_product.name)
        if index != -1:
            self.products[index].quantity += quantity
        else:
            self.products.append(new_product)

    def minus(self, product_name, quantity):
        index = self.search_products(product_name)
        if index != -1:
            self.products[index].quantity -= quantity
            if self.products[index].quantity <= 0:
                del self.products[index]

    def sum_price(self):
        return sum(product.sum_price() for product in self.products)

    def search_products(self, name):
        for i, product in enumerate(self.products):
            if product.name == name:
                return i
        return -1

    def to_dict(self):
        return {
            "name": self.name,
            "products": [p.to_dict() for p in self.products]
        }

    @classmethod
    def from_dict(cls, data):
        table = Table(data["name"])
        table.products = [Product.from_dict(p) for p in data["products"]]
        return table

    def generate_receipt_image(self):
        # 設定
        width = 384*2  # レシートプリンタ幅に合わせたピクセル数（一般的）
        padding = 100
        line_height = 30
        font_size = 48

        # フォントの指定（環境に合わせてパスを変更）
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", font_size)
            print("日本語フォント読み込み成功")
        except Exception as e:
            print("フォント読み込み失敗:", e)
            font = ImageFont.load_default()

        # レシートに出力するテキスト行の準備
        lines = []
        lines.append("★ レシート ★")
        lines.append(f"テーブル: {self.name}")
        lines.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        lines.append("-" * 32)

        for product in self.products:
            name = product.name
            quantity = product.quantity
            price = product.price
            total = product.sum_price()
            lines.append(f"{name} x{quantity}")
            lines.append(f"  {price}円 x {quantity} = {total}円")

        lines.append("-" * 32)
        total_price = self.sum_price()
        lines.append(f"合計: {total_price}円")
        lines.append("ありがとうございました！")

        # 画像サイズの計算
        height = padding * 2 + line_height * len(lines)

        # 画像の作成（白背景）
        image = Image.new("L", (width, height), color=255)
        draw = ImageDraw.Draw(image)

        # テキスト描画（黒文字）
        y = padding
        for line in lines:
            draw.text((padding, y), line, font=font, fill=0)
            y += line_height

        return image

# テーブル管理
class TablesManager:
    def __init__(self):
        self.tables = []

    def add(self, name):
        self.tables.append(Table(name))

    def get(self, i):
        return self.tables[i]

    def get_name_list(self):
        return [table.name for table in self.tables]
    
    def to_dict(self):
        return [table.to_dict() for table in self.tables]

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def load_from_file(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.tables = [Table.from_dict(t) for t in data]
# UI
class table_view:
    def __init__(self, root, productdatabase, tablesmanager, category_db, am):  # ← ここに category_db を追加
        self.root = root
        self.pdb = productdatabase
        self.tm = tablesmanager
        self.category_db = category_db
        self.am = am
        self.tableOBJs = []
        self.Selected_Table_Combo = -1
        self.product_frames = []

        self.Table_Area_Init()

        self.NewTable_Input = tk.Entry(self.root, font=("Helvetica", 12))
        self.NewTable_Input.pack(pady=5)

        self.Add_Table_Button = tk.Button(
            self.root, text="＋ テーブル追加", font=("Helvetica", 12, "bold"),
            command=self.add_new_table, bg="#cde", padx=10, pady=5
        )
        self.Add_Table_Button.pack(pady=5)


    def Table_Combo_On_Selected(self, event=None):
        self.Selected_Table_Combo = self.Table_Combo.get()
        self.Table_Data_Set(self.Selected_Table_Combo)
        return self.Selected_Table_Combo

    def Table_Area_Init(self):

        self.Table_Combo = ttk.Combobox(self.root, values=self.tm.get_name_list(), font=("Helvetica", 12))
        self.Table_Combo.pack(pady=10)
        self.Table_Combo.bind('<<ComboboxSelected>>', self.Table_Combo_On_Selected)

        # スクロール可能なキャンバスとフレームを作成
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, borderwidth=0, height=500)  # 必要に応じて高さ調整
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # 内部の実際のフレーム（これにウィジェットを追加していく）
        self.Table_Area_Frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.Table_Area_Frame, anchor="nw")

        # フレームサイズが変わったときにスクロール範囲を更新
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.Table_Area_Frame.bind("<Configure>", on_configure)

        # ホイールでスクロール（Windows / Mac 対応）
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)         # Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux


        #self.Table_Area_Frame = tk.Frame(canvas, bg="#f0f0f0", padx=10, pady=10)
        #self.Table_Area_Frame.pack(fill=tk.BOTH, expand=True)

        self.Table_Sum = tk.Label(self.Table_Area_Frame, text="合計: ¥0", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
        self.Table_Sum.grid(row=999, column=0, pady=10, sticky="w")

        self.Table_Accounting_button = tk.Button(canvas_frame, text="会計", font=("Helvetica", 12, "bold"), command=self.Table_Accout)
        self.Table_Accounting_button.pack()

    def Table_Accout(self):
        table_id = self.get_current_table()
        if table_id is None:
            return
        table = self.tm.tables[table_id]
        if not table.products:
            return

        self.newWindow = tk.Toplevel(self.root)
        app = AccountingView(self.newWindow, self, self.tm, self.am)
        # 会計処理をここに追加
        

    def Table_Data_Set(self, table_name):
        self.tableOBJs_all_destroy()
        self.tableOBJs = []

        for table in self.tm.tables:
            if table.name == table_name:
                table_products = table.products
                table = table
                break
        else:
            return

        for i, product in enumerate(table_products):
            self.Add_to_table_obj(product)

        self.Table_Sum["text"] = f"合計: ¥{table.sum_price()}"

    def Add_to_table_obj(self, table_product):
        category_color = self.category_db.get_color(table_product.category)  # ← ここを変更

        product_frame = tk.Frame(self.Table_Area_Frame, bg=category_color, padx=5, pady=5, relief=tk.RIDGE, bd=2)
        product_frame.grid_propagate(False)
        product_frame.config(width=600, height = 50)

        product_frame.grid(row=len(self.product_frames), column=0, pady=3, sticky="w")
        self.product_frames.append(product_frame)

        label_name = tk.Label(product_frame, text=table_product.name, font=("Helvetica", 15, "bold"),
                              width=10, anchor="w", bg=category_color)
        label_name.grid(row=0, column=0)

        label_unitprice = tk.Label(product_frame, text=f"¥{table_product.price}", font=("Helvetica", 15),
                                   width=10, anchor="e", bg=category_color)
        label_unitprice.grid(row=0, column=1)

        button_minus = tk.Button(product_frame, text="-", command=lambda name=table_product.name: self.minus_button(name),
                                 font=("Helvetica", 10), bg="#ffffff", width=3)
        button_minus.grid(row=0, column=2)

        label_quantity = tk.Label(product_frame, text=table_product.quantity, font=("Helvetica", 16),
                                  width=3, anchor="e", bg=category_color)
        label_quantity.grid(row=0, column=3)

        button_plus = tk.Button(product_frame, text="+", command=lambda name=table_product.name: self.plus_button(name),
                                font=("Helvetica", 10), bg="#ffffff", width=3)
        button_plus.grid(row=0, column=4)

        label_sumprice = tk.Label(product_frame, text=f"¥{table_product.sum_price()}", font=("Helvetica", 20),
                                  width=10, anchor="e", bg=category_color)
        label_sumprice.grid(row=0, column=5)

        self.tableOBJs.append({
            "label_name": label_name,
            "label_unitprice": label_unitprice,
            "button_minus": button_minus,
            "label_quantity": label_quantity,
            "button_plus": button_plus,
            "label_sumprice": label_sumprice
        })

    def tableOBJs_all_destroy(self):
        for obj in self.tableOBJs:
            for widget in obj.values():
                widget.destroy()
        for frame in self.product_frames:
            frame.destroy()
        self.tableOBJs = []
        self.product_frames = []

    def search_table(self, name):
        for i, table in enumerate(self.tm.tables):
            if table.name == name:
                return i
        return None

    def get_current_table(self):
        i = self.search_table(self.Selected_Table_Combo)
        return i

    def search_product_in_table(self, table_name, product_name):
        table_id = self.get_current_table()
        for i, product in enumerate(self.tm.tables[table_id].products):
            if product.name == product_name:
                return i
        return None

    def search_productlabel_in_table(self, product_name):
        for i, OBJ in enumerate(self.tableOBJs):
            if OBJ["label_name"]["text"] == product_name:
                return i
        return None

    def update(self, product_name):
        table_id = self.get_current_table()
        product_id = self.search_product_in_table(self.Selected_Table_Combo, product_name)

        if product_id is None:
            id = self.search_productlabel_in_table(product_name)
            if id is not None:
                for widget in self.tableOBJs[id].values():
                    widget.destroy()
                self.tableOBJs.pop(id)
                self.product_frames[id].destroy()
                self.product_frames.pop(id)
        else:
            self.tableOBJs[product_id]["label_quantity"]["text"] = str(self.tm.tables[table_id].products[product_id].quantity)
            self.tableOBJs[product_id]["label_sumprice"]["text"] = f"¥{self.tm.tables[table_id].products[product_id].sum_price()}"
        self.Table_Sum["text"] = f"合計: ¥{self.tm.tables[table_id].sum_price()}"

    def plus_button(self, product_name):
        table_id = self.get_current_table()
        product_index_in_db = next((i for i, p in enumerate(self.pdb.products) if p.name == product_name), None)
        if product_index_in_db is not None:
            self.tm.tables[table_id].buy(self.pdb, product_index_in_db, 1)
        self.update(product_name)

    def minus_button(self, product_name):
        table_id = self.get_current_table()
        self.tm.tables[table_id].minus(product_name, 1)
        self.update(product_name)

    def buy(self, i):
        table_id = self.get_current_table()
        product_id = self.search_product_in_table(self.Selected_Table_Combo, self.pdb.products[i].name)
        self.tm.tables[table_id].buy(self.pdb, i, 1)
        if product_id is None:
            self.Add_to_table_obj(self.pdb.products[i])
        else:
            self.update(self.pdb.products[i].name)
        self.Table_Sum["text"] = f"合計: ¥{self.tm.tables[table_id].sum_price()}"

    def add_new_table(self):
        new_table_name = self.NewTable_Input.get().strip()
        if not new_table_name:
            return  # 空なら何もしない

        if new_table_name in self.tm.get_name_list():
            return  # 重複テーブル名は追加しない

        self.tm.add(new_table_name)
        self.Table_Combo['values'] = self.tm.get_name_list()
        self.Table_Combo.set(new_table_name)
        self.Table_Data_Set(new_table_name)
        self.NewTable_Input.delete(0, tk.END)

class products_view:
    def __init__(self, root, product_db, table_view, category_db):
        self.root = root
        self.pdb = product_db
        self.tv = table_view
        self.category_db = category_db
        self.button_set()


    def button_set(self):
        # スクロール可能なキャンバスとフレームを作成
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, borderwidth=0, height=500)  # 必要に応じて高さ調整
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # 内部の実際のフレーム（これにウィジェットを追加していく）
        self.button_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.button_frame, anchor="nw")

        # フレームサイズが変わったときにスクロール範囲を更新
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.button_frame.bind("<Configure>", on_configure)

        # ホイールでスクロール（Windows / Mac 対応）
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)         # Windows
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

        # --- 以下はカテゴリごとのボタン生成 ---
        categorized_products = {}
        for i, product in enumerate(self.pdb.products):
            categorized_products.setdefault(product.category, []).append((i, product))

        for category in sorted(categorized_products.keys()):
            products = categorized_products[category]
            category_name = self.category_db.get_name(category)
            category_color = self.category_db.get_color(category)

            label = tk.Label(
                self.button_frame, 
                text=category_name,
                font=("Helvetica", 14, "bold"),
                bg=category_color, 
                anchor="w",
                padx=10
            )
            label.pack(fill="x", pady=(10, 0))

            category_frame = tk.Frame(self.button_frame, bg=category_color, pady=5)
            category_frame.pack(fill="x", padx=10, pady=(0, 10))

            for idx, (i, product) in enumerate(products):
                button = tk.Button(
                    category_frame,
                    text=f"{product.name}\n¥{product.price}",
                    command=lambda i=i: self.tv.buy(i),
                    font=("Helvetica", 15),
                    bg=category_color,
                    activebackground="#ccc",
                    relief=tk.RAISED,
                    borderwidth=2,
                    highlightthickness=1,
                    padx=10,
                    pady=10,
                    width=12,
                    height=2
                )
                button.grid(row=idx // 3, column=idx % 3, padx=5, pady=5)

class ScreenTenKey:
    def __init__(self, parent_frame, target_label, on_confirm=None):
        self.parent_frame = parent_frame  # テンキーを挿入するフレーム
        self.target_label = target_label  # 数字を表示するラベル
        self.on_confirm = on_confirm      # 確定時のコールバック関数（任意）

        self.input_value = ""
        self.frame = tk.Frame(self.parent_frame)
        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('←', 3, 0), ('0', 3, 1), ('OK', 3, 2),
        ]

        for (text, row, col) in buttons:
            btn = tk.Button(self.frame, text=text, width=5, height=2,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def on_button_click(self, char):
        if char.isdigit():
            self.input_value += char
        elif char == '←':
            self.input_value = self.input_value[:-1]
        elif char == 'OK':
            if self.on_confirm:
                self.on_confirm(self.input_value)
        self.update_label()

    def update_label(self):
        self.target_label.config(text=self.input_value)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def place(self, **kwargs):
        self.frame.place(**kwargs)

class AccountingView:
    def __init__(self, root, table_view, tables_manager, archived_manager):
        self.root = root
        self.tv = table_view
        self.tm = tables_manager
        self.am = archived_manager

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.label_info = tk.Label(self.frame, text="支払い金額を入力してください", font=("Courier", 14))
        self.label_info.pack()


        table_id = self.tv.search_table(self.tv.Selected_Table_Combo)
        if table_id is None:
            return
        self.current_sum = self.tm.tables[table_id].sum_price()

        self.label_sum = tk.Label(self.frame, text=f"合計金額: {self.current_sum}円", font=("Courier", 14))
        self.label_sum.pack(pady=5)

        self.label_input = tk.Label(self.frame, text="", font=("Courier", 24), bg="white", width=10)
        self.label_input.pack(pady=5)

        self.label_change = tk.Label(self.frame, text="", font=("Courier", 14))
        self.label_change.pack(pady=5)

        self.tenkey = ScreenTenKey(self.frame, self.label_input, on_confirm=self.on_confirm)
        self.tenkey.pack()

        self.button_finalize = tk.Button(self.frame, text="会計確定", command=self.finalize_transaction, state="disabled")
        self.button_finalize.pack(pady=5)


    def on_confirm(self, input_text):
        if not input_text.isdigit():
            self.label_change.config(text="無効な入力")
            return
        payment = int(input_text)
        change = payment - self.current_sum
        print(self.current_sum)
        if change < 0:
            self.label_change.config(text=f"不足：{-change}円")
            self.button_finalize.config(state="disabled")
        else:
            self.label_change.config(text=f"お釣り：{change}円")
            self.button_finalize.config(state="normal")

    def finalize_transaction(self):
        table_id = self.tv.search_table(self.tv.Selected_Table_Combo)
        if table_id is None:
            return
        table = self.tm.tables[table_id]
        self.tm.tables[table_id].generate_receipt_image().save(f"{table.name}_receipt_{time.time()}.png")
        self.am.archive(table)
        table.products = []
        self.tv.Table_Data_Set(table.name)
        self.label_info.config(text="会計完了しました！")
        self.label_change.config(text="")
        self.label_input.config(text="")
        self.button_finalize.config(state="disabled")
        

class POSApp:
    def __init__(self, root, pdb, tm):
        self.root = root
        self.root.title("レジ会計システム")
        self.root.geometry("1200x700")

        self.pdb = pdb
        self.tm = tm
        self.am = ArchivedManager()

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # 3カラムレイアウト
        self.left_frame = tk.Frame(self.main_frame, width=600, height=600, bg="#fff")
        self.center_frame = tk.Frame(self.main_frame, width=600, height=1200)
        #self.right_frame = tk.Frame(self.main_frame, width=400, bg="#f0f0f0")

        self.left_frame.propagate(False)
        self.center_frame.propagate(False)

        self.left_frame.pack(side="left")
        self.center_frame.pack(side="left", fill="both", expand=True)
        #self.right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # 各ビューの初期化
        self.category_db = CategoryDB()
        self.table_view = table_view(self.left_frame, self.pdb, self.tm, self.category_db, self.am)
        
        self.products_view = products_view(self.center_frame, self.pdb, self.table_view, self.category_db)
        #self.accounting_view = AccountingView(self.right_frame, self.table_view, self.tm, self.am)



if __name__ == "__main__":
    ProductDatabase = ProductDatabase()
    TablesManager = TablesManager()

    # ファイルが存在すれば読み込む
    if os.path.exists("products.json"):
        ProductDatabase.load_from_file("products.json")
    else:
        # 初期データ
        ProductDatabase.add("cake", 100, 0)
        ProductDatabase.add("coffee", 100, 1)

    if os.path.exists("tables.json"):
        TablesManager.load_from_file("tables.json")
    else:
        for i in range(1, 20):
            TablesManager.add(f"Table {i}")
        TablesManager.add("Takeout")

    root = tk.Tk()
    root.geometry("1280x800")
    app = POSApp(root, ProductDatabase, TablesManager)

    # アプリ終了時に保存
    def on_closing():
        ProductDatabase.save_to_file("products.json")
        TablesManager.save_to_file("tables.json")
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()