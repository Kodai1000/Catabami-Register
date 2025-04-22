import tkinter as tk
from tkinter import messagebox, colorchooser
import json
import os

CATEGORY_FILE = "category_labels.json"

class CategoryEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("カテゴリ編集アプリ")
        self.categories = {}
        self.load_categories()

        self.listbox = tk.Listbox(root, width=50, font=("Helvetica", 12))
        self.listbox.pack(pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="追加", command=self.add_category).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="編集", command=self.edit_category).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="削除", command=self.delete_category).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="保存", command=self.save_categories).grid(row=0, column=3, padx=5)

        self.refresh_listbox()

    def load_categories(self):
        if os.path.exists(CATEGORY_FILE):
            with open(CATEGORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.categories = {int(k): v for k, v in data.items()}
        else:
            self.categories = {}

    def save_categories(self):
        data = {str(k): v for k, v in self.categories.items()}
        with open(CATEGORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("保存完了", "category_labels.json に保存されました。")

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for cid, info in sorted(self.categories.items()):
            self.listbox.insert(tk.END, f'{cid}: {info["name"]} - {info["color"]}')

    def open_form(self, title, on_submit, name="", color="#ffffff"):
        form = tk.Toplevel(self.root)
        form.title(title)
        form.grab_set()

        tk.Label(form, text="カテゴリ名").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(form)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, name)

        tk.Label(form, text="色").grid(row=1, column=0, padx=10, pady=5)
        color_entry = tk.Entry(form)
        color_entry.grid(row=1, column=1, padx=10, pady=5)
        color_entry.insert(0, color)

        def choose_color():
            chosen_color = colorchooser.askcolor(initialcolor=color_entry.get())[1]
            if chosen_color:
                color_entry.delete(0, tk.END)
                color_entry.insert(0, chosen_color)

        tk.Button(form, text="色を選ぶ", command=choose_color).grid(row=1, column=2, padx=5)

        def submit():
            try:
                cat_name = name_entry.get().strip()
                cat_color = color_entry.get().strip()
                if not cat_name or not cat_color:
                    raise ValueError("カテゴリ名と色は必須です。")
                on_submit(cat_name, cat_color)
                form.destroy()
            except Exception as e:
                messagebox.showerror("エラー", str(e))

        tk.Button(form, text="確定", command=submit).grid(row=2, column=0, columnspan=3, pady=10)

    def add_category(self):
        def on_submit(name, color):
            next_id = max(self.categories.keys(), default=-1) + 1
            self.categories[next_id] = {"name": name, "color": color}
            self.refresh_listbox()
        self.open_form("カテゴリを追加", on_submit)

    def edit_category(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("選択エラー", "編集するカテゴリを選んでください。")
            return
        cid = int(self.listbox.get(selection[0]).split(":")[0])
        cat = self.categories[cid]
        def on_submit(name, color):
            self.categories[cid] = {"name": name, "color": color}
            self.refresh_listbox()
        self.open_form("カテゴリを編集", on_submit, cat["name"], cat["color"])

    def delete_category(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("選択エラー", "削除するカテゴリを選んでください。")
            return
        cid = int(self.listbox.get(selection[0]).split(":")[0])
        if messagebox.askyesno("確認", f"カテゴリ {cid} を削除しますか？"):
            del self.categories[cid]
            self.refresh_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = CategoryEditorApp(root)
    root.mainloop()
