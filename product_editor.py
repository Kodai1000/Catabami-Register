import tkinter as tk
from tkinter import messagebox
import json
import os

PRODUCTS_FILE = "products.json"
CATEGORY_FILE = "category_labels.json"

class ProductEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("商品編集アプリ")
        self.products = []
        self.category_labels = self.load_category_labels()
        
        self.listbox = tk.Listbox(root, width=50, font=("Helvetica", 12))
        self.listbox.pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="追加", command=self.add_product).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="編集", command=self.edit_product).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="削除", command=self.delete_product).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="保存", command=self.save_products).grid(row=0, column=3, padx=5)

        self.load_products()
        self.refresh_listbox()

    def load_category_labels(self):
        if os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {int(k): v for k, v in data.items()}
        else:
            return {
                0: {"name": "スイーツ", "color": "#ffd1dc"},
                1: {"name": "ドリンク", "color": "#d0f0fd"},
                2: {"name": "その他", "color": "#d3f9d8"}
            }

    def load_products(self):
        if os.path.exists(PRODUCTS_FILE):
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                self.products = json.load(f)
        else:
            self.products = []

    def save_products(self):
        with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("保存完了", "products.json に保存されました。")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for product in self.products:
            cat_name = self.category_labels.get(product["category"], {}).get("name", "不明")
            self.listbox.insert(tk.END, f'{product["name"]} - ¥{product["price"]} [{cat_name}]')

    def open_product_form(self, title, on_submit, product=None):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.grab_set()

        tk.Label(form, text="商品名").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(form)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="価格").grid(row=1, column=0, padx=10, pady=5)
        price_entry = tk.Entry(form)
        price_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="カテゴリ").grid(row=2, column=0, padx=10, pady=5)
        category_var = tk.IntVar()

        category_keys = list(self.category_labels.keys())
        # カテゴリ名とIDを表示するリストを作成
        category_names = [f"{self.category_labels[k]['name']} ({k})" for k in category_keys]

        # OptionMenuにはカテゴリIDのみを渡すが、表示には名前を使用
        category_menu = tk.OptionMenu(form, category_var, *category_keys)
        category_menu.grid(row=2, column=1, padx=10, pady=5)

        # 初期値を設定
        if product:
            name_entry.insert(0, product["name"])
            price_entry.insert(0, str(product["price"]))
            category_var.set(product["category"])
        else:
            category_var.set(0)

        def submit():
            try:
                name = name_entry.get()
                price = int(price_entry.get())
                category = category_var.get()
                if not name:
                    raise ValueError("商品名が空です")
                on_submit(name, price, category)
                form.destroy()
            except Exception as e:
                messagebox.showerror("エラー", f"入力に誤りがあります: {e}")

        tk.Button(form, text="確定", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

    def add_product(self):
        def on_submit(name, price, category):
            self.products.append({"name": name, "price": price, "category": category, "quantity": 1})
            self.refresh_listbox()
        self.open_product_form("商品を追加", on_submit)

    def edit_product(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("選択エラー", "編集する商品を選択してください。")
            return

        original = self.products[index[0]]

        def on_submit(name, price, category):
            self.products[index[0]] = {"name": name, "price": price, "category": category, "quantity": 1}
            self.refresh_listbox()

        self.open_product_form("商品を編集", on_submit, original)

    def delete_product(self):
        index = self.listbox.curselection()
        if not index:
            messagebox.showwarning("選択エラー", "削除する商品を選んでください。")
            return
        del self.products[index[0]]
        self.refresh_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductEditorApp(root)
    root.mainloop()
