import json
import random
import string

def show_menu():
    print("1 - Generate new password\n""2 - All password\n""3 - Clear all password\n""4 - Exit")
def load_data():
    try:
        with open('data.json','r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

def generate_password(length):
    alphabet = string.ascii_letters + string.digits 
    return ''.join(random.choice(alphabet) for _ in range(length))

def show_password():
    sp = load_data()
    if not sp:
        print('Password None')
    else:
        print('ALL PASSWORD')
        for x,pwd in enumerate(sp,start=1):
            print(f"{x}:{pwd}")

def delete_all():
    save_data([])
    print('All password delete')
def main():
    while True:
        show_menu()
        try:
            choice = int(input('Enter num in menu:'))
            if choice == 1:
                length  = int(input('Enter len:'))
                passw = generate_password(length)
                print(passw)
                data = load_data()#запомнить - вначале загрузили джсон,потом добавили,потом перезаписали!
                data.append(passw)#запомнитить-добавление к джсону
                save_data(data)
            elif choice == 2:
                show_password()
            elif choice == 3:
                delete_all()
            elif choice ==4:
                break
            else:
                 print('Enter num(1-4)!')
        except ValueError:
            print('Enter num(1-4)!')

main()
