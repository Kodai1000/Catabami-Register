import tkinter as tk

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

if __name__ == "__main__":
    def on_confirmed(value):
        print(f"確定された値: {value}")

    root = tk.Tk()
    root.title("テンキー（フレーム指定）")

    # 上部にラベル
    label = tk.Label(root, text="", font=("Arial", 24), bg="white", width=10)
    label.pack(pady=10)

    # テンキー用フレームを別に作る
    keypad_frame = tk.Frame(root)
    keypad_frame.pack()

    # テンキーを特定のフレームに挿入
    tenkey = ScreenTenKey(parent_frame=keypad_frame, target_label=label, on_confirm=on_confirmed)
    tenkey.pack()

    root.mainloop()
