import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_index = listbox.curselection()
    if selected_index:
        i = selected_index[0]
        label.config(text=f"This is the content of Item {i+1}")

root = tk.Tk()
root.title("List Selector Example")
root.geometry("600x400")

# 左側のリスト
listbox = tk.Listbox(root, width=25)
for i in range(1, 51):
    listbox.insert(tk.END, f"Item {i}")
listbox.pack(side=tk.LEFT, fill=tk.Y)
listbox.bind('<<ListboxSelect>>', on_select)

# 右側の表示エリア
content_frame = ttk.Frame(root)
content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

label = ttk.Label(content_frame, text="Select an item from the list")
label.pack(padx=10, pady=10)

root.mainloop()
