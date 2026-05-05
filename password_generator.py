import random
import string
import json
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("750x550")
        self.root.resizable(False, False)
        
        # Цветовая схема
        self.root.configure(bg="#f0f0f0")
        
        # История паролей
        self.history_file = "password_history.json"
        self.history = self.load_history()
        
        # Создание интерфейса
        self.create_widgets()
        self.update_history_table()
    
    def create_widgets(self):
        # Заголовок
        title_label = Label(self.root, text="🔐 Генератор случайных паролей", 
                           font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title_label.pack(pady=10)
        
        # Рамка настроек
        settings_frame = LabelFrame(self.root, text="Настройки пароля", 
                                   padx=15, pady=15, font=("Arial", 11, "bold"),
                                   bg="#f0f0f0", fg="#333")
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        # Ползунок длины пароля
        Label(settings_frame, text="Длина пароля:", font=("Arial", 10),
              bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        
        self.length_var = IntVar(value=12)
        self.length_slider = Scale(settings_frame, from_=4, to=50, orient=HORIZONTAL,
                                   variable=self.length_var, length=350, bg="#f0f0f0",
                                   activebackground="#4CAF50", troughcolor="#ddd")
        self.length_slider.grid(row=0, column=1, padx=10, pady=5)
        
        self.length_label = Label(settings_frame, text="12", font=("Arial", 10, "bold"),
                                  bg="#f0f0f0", fg="#4CAF50", width=5)
        self.length_label.grid(row=0, column=2, pady=5)
        self.length_slider.configure(command=lambda x: self.length_label.config(text=str(int(float(x)))))
        
        # Чекбоксы
        self.use_digits = BooleanVar(value=True)
        self.use_letters = BooleanVar(value=True)
        self.use_punctuation = BooleanVar(value=False)
        
        Checkbutton(settings_frame, text="📊 Цифры (0-9)", variable=self.use_digits,
                   bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        
        Checkbutton(settings_frame, text="🔤 Буквы (A-Z, a-z)", variable=self.use_letters,
                   bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=1, sticky="w", pady=5)
        
        Checkbutton(settings_frame, text="✨ Спецсимволы (!@#$%^&*)", variable=self.use_punctuation,
                   bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=2, sticky="w", pady=5)
        
        # Кнопка генерации
        self.generate_btn = Button(self.root, text="Сгенерировать пароль", 
                                   command=self.generate_password,
                                   bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                   padx=20, pady=8, cursor="hand2", relief=RAISED, bd=2)
        self.generate_btn.pack(pady=10)
        
        # Поле для отображения пароля
        password_frame = Frame(self.root, bg="#f0f0f0")
        password_frame.pack(pady=10)
        
        Label(password_frame, text="Сгенерированный пароль:", font=("Arial", 10),
              bg="#f0f0f0").pack()
        
        self.password_var = StringVar()
        self.password_entry = Entry(password_frame, textvariable=self.password_var, 
                                   font=("Courier", 14, "bold"), state="readonly", 
                                   justify="center", width=40, relief=SUNKEN, bd=2)
        self.password_entry.pack(pady=5)
        
        # Кнопка копирования
        self.copy_btn = Button(password_frame, text="📋 Копировать в буфер", 
                              command=self.copy_to_clipboard,
                              bg="#2196F3", fg="white", font=("Arial", 10),
                              padx=15, pady=5, cursor="hand2")
        self.copy_btn.pack(pady=5)
        
        # Таблица истории
        history_frame = LabelFrame(self.root, text="📜 История паролей", 
                                  padx=10, pady=10, font=("Arial", 11, "bold"),
                                  bg="#f0f0f0", fg="#333")
        history_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Создание таблицы с прокруткой
        tree_frame = Frame(history_frame, bg="#f0f0f0")
        tree_frame.pack(fill="both", expand=True)
        
        columns = ("#", "Пароль", "Длина", "Тип символов", "Дата генерации")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        # Настройка колонок
        self.tree.heading("#", text="#")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Тип символов", text="Тип символов")
        self.tree.heading("Дата генерации", text="Дата генерации")
        
        self.tree.column("#", width=40, anchor="center")
        self.tree.column("Пароль", width=180, anchor="center")
        self.tree.column("Длина", width=60, anchor="center")
        self.tree.column("Тип символов", width=150, anchor="center")
        self.tree.column("Дата генерации", width=170, anchor="center")
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")
        
        # Кнопки управления историей
        btn_frame = Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)
        
        Button(btn_frame, text="🗑️ Очистить историю", command=self.clear_history,
               bg="#f44336", fg="white", font=("Arial", 10), padx=15, pady=5,
               cursor="hand2").pack(side=LEFT, padx=5)
        
        Button(btn_frame, text="💾 Сохранить историю", command=self.save_history,
               bg="#FF9800", fg="white", font=("Arial", 10), padx=15, pady=5,
               cursor="hand2").pack(side=LEFT, padx=5)
    
    def generate_password(self):
        """Генерация случайного пароля"""
        length = self.length_var.get()
        chars = ""
        
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_punctuation.get():
            chars += string.punctuation
        
        # Проверка корректности ввода
        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return
        
        if length < 4 or length > 50:
            messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 50 символов!")
            return
        
        # Генерация пароля
        password = ''.join(random.choice(chars) for _ in range(length))
        
        # Запись в историю
        self.password_var.set(password)
        self.add_to_history(password, length, self.get_selected_chars())
        
        # Визуальный эффект
        self.generate_btn.config(bg="#45a049")
        self.root.after(200, lambda: self.generate_btn.config(bg="#4CAF50"))
    
    def get_selected_chars(self):
        """Получение выбранных типов символов в виде строки"""
        types = []
        if self.use_digits.get():
            types.append("цифры")
        if self.use_letters.get():
            types.append("буквы")
        if self.use_punctuation.get():
            types.append("спецсимволы")
        return ", ".join(types)
    
    def add_to_history(self, password, length, char_types):
        """Добавление пароля в историю"""
        record = {
            "password": password,
            "length": length,
            "char_types": char_types,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(record)
        self.save_history()
        self.update_history_table()
    
    def update_history_table(self):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Заполнение таблицы (новые сверху)
        for idx, record in enumerate(self.history[::-1], 1):
            self.tree.insert("", "end", values=(
                idx,
                record["password"],
                record["length"],
                record["char_types"],
                record["date"]
            ))
    
    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Успех", "✅ Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Сначала сгенерируйте пароль!")
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю паролей?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Готово", "История успешно очищена!")

if __name__ == "__main__":
    root = Tk()
    app = PasswordGenerator(root)
    root.mainloop()
