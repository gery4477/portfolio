import json
from datetime import datetime
from datetime import date,timedelta
from tkinter import ttk, messagebox, simpledialog
import tkinter as tk



def show_menu():
    print("1 - Добавить расход\n"
          "2 - Добавить доход\n"
          "3 - Показать баланс\n"
          "4 - Показать статистику за период\n"
          "5 - Показать топ категорий\n"
          "6 - Удалить запись по ID\n"
          "7 - Показать все записи\n"
          "8 - Выход\n")
def load_data():
    try:
        with open('data.json','r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_data(data):
    try:
        with open('data.json', 'w') as f:
           json.dump(data, f, indent=4)
    except Exception as e:
        print(f'Ошибка сохранения: {e}')
def add_expense(category,amount):
    data = load_data()
    dates = datetime.now().strftime('%Y-%m-%d')
    x = len(data) + 1
    new_entry = {
        'id':x,
        'type':'Расход',
        'category':category,
        'amount':amount,
        'date':dates
    }
    data.append(new_entry)
    save_data(data)
def add_transaction(category,amount):
    try:
        data = load_data()
        dates = datetime.now().strftime('%Y-%m-%d')
        x = len(data) + 1
        new_entr = {
            'id': x,
            'type': 'Доход',
            'category': category,
            'amount': amount,
            'date': dates
        }
        data.append(new_entr)
        save_data(data)
    except ValueError:
        print('Пожалуйста введите число')
    except Exception as e:
        print(f'Ошибка{e}')
def balance():
    data = load_data()
    income = 0
    expense = 0
    for x in data:
        if x['type'] == 'Расход':
            expense += x['amount']
        elif x['type'] == 'Доход':
            income += x['amount']
    balance = income - expense
    print(f'Доходы:{income}')
    print(f'Расходы:{expense}')
    print(f'Баланс:{balance}')
    return income,expense,balance
def show_stat():
    today = date.today()
    week_ago = today - timedelta(days=7)
    data = load_data()
    try:
        user_data = int(input('Выберите период:\n'
                     '1 - день\n'
                     '2 - неделя\n'
                     '3 - месяц:\n'))
        if user_data == 1:
            start_date = today
            end_date = today
        elif user_data == 2:
            start_date = week_ago
            end_date = today
        elif user_data == 3:
            start_date = today.replace(day=1)
            end_date = today
        else:
            print('Введите цифру 1-3!')
    except ValueError:
        print('Введите цифру от 1 до 3!')
    filtered = []
    for record in data:
        record_date = datetime.strptime(record['date'], '%Y-%m-%d').date()
        if start_date <= record_date <= end_date:
            filtered.append(record)
    income = 0
    expense = 0
    for x in filtered:
        if x['type'] == 'Расход':
            expense += x['amount']
        elif x['type'] == 'Доход':
            income += x['amount']
    bal = income - expense
    print(f'Доходы за  ваш период:{income}')
    print(f'Расходы:{expense}')
    return filtered
def top_category():
    data = load_data()
    filtered = []
    for record in data:
        if record['type'] == 'Расход':
            filtered.append(record)
    categories = {}
    for record in filtered:
        categories[record['category']] = categories.get(record['category'],0) +int(record['amount'])
    items = list(categories.items())
    items.sort(key=lambda x:x[1],reverse=True)
    top = items[:5]
    print(f'Топ 5 категорий за все время:')
    for i,(category,amount) in enumerate(top,start=1):
        print(f'{i},{category}:{amount} руб')#распаковка списка с кортежем
def delete_id():
    data = load_data()
    for x in data:
        print(f'ID:{x['id']}|{x['date']}|{x['type']}|{x['category']}|{x['amount']} руб')
    try:
        us_id = int(input('Введите нужное id:'))
        for index,x in enumerate(data) :
            if x['id'] == us_id:
                data.pop(index)
                save_data(data)
                print('Запись удалена успешно!')
                return
        print('Запись с таким id не найдена')
    except ValueError:
        print('Введите пожалуйста число id!')
def show_all():
    data = load_data()
    for x in data:
        print(f'ID:{x['id']}|{x['date']}|{x['type']}|{x['category']}|{x['amount']} руб')
    return
def add_record():
    category = entry_category.get().strip()
    amount_str = entry_amount.get().strip()
    trans_type = type_var.get()
    if not category or not amount_str:
        print('Заполните все поля!')
        return
    try:
        amount = float(amount_str)
    except ValueError:
        print('Введите сумму в виде числа!')
    if trans_type == 'Расход':
        add_expense(category,amount)
    else:
        add_transaction(category,amount)
    entry_category.delete(0,tk.END)
    entry_amount.delete(0, tk.END)
    update_table()
def update_table():
    tree.delete(*tree.get_children())
    data = load_data()
    for record in data:
        tree.insert('','end',values=(record['id'],record['date'],record['type'],record['category'],record['amount']))
    return
def show_balance():
    data = load_data()
    income = 0
    expense = 0
    for x in data:
        if x['type'] == 'Расход':
            expense += x['amount']
        elif x['type'] == 'Доход':
            income += x['amount']
    balance = income - expense
    messagebox.showinfo('Баланс',f'Доходы:{income}\nРасходы:{expense}\nБаланс:{balance}')
def delete_record():
    record_id = simpledialog.askinteger('Удаление','Введите ID для удаления записи:')
    if record_id is None:
        return
    data = load_data()
    for index, x in enumerate(data):
        if x['id'] == record_id:
            data.pop(index)
            save_data(data)
            print('Запись удалена успешно!')
            update_table()
            return
    messagebox.showerror('Ошибка',f'Запись с ID {record_id} Не найдена.')

root = tk.Tk()
root.title("Трекер расходов")
root.geometry("700x500")

# Метки и поля ввода
tk.Label(root, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
entry_category = tk.Entry(root)
entry_category.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Сумма:").grid(row=1, column=0, padx=5, pady=5)
entry_amount = tk.Entry(root)
entry_amount.grid(row=1, column=1, padx=5, pady=5)

# Выбор типа
tk.Label(root, text="Тип:").grid(row=2, column=0, padx=5, pady=5)
type_var = tk.StringVar(value="Расход")
ttk.Combobox(root, textvariable=type_var, values=["Расход", "Доход"]).grid(row=2, column=1, padx=5, pady=5)

# Кнопки
tk.Button(root, text="Добавить", command=add_record).grid(row=3, column=0, padx=5, pady=5)
tk.Button(root, text="Обновить", command=update_table).grid(row=3, column=1, padx=5, pady=5)
tk.Button(root, text="Баланс", command=show_balance).grid(row=3, column=2, padx=5, pady=5)
tk.Button(root, text="Удалить по ID", command=delete_record).grid(row=3, column=3, padx=5, pady=5)

# Таблица
columns = ("ID", "Дата", "Тип", "Категория", "Сумма")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()





