import json

def show_menu():
    print("1 - add password\n""2 - all password\n""3 - search password in name service\n""4 - delete password in name service\n""5 - exit")
def load_data():
    try:
        with open('data.json','r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def save_data(data):
    with open('data.json','w') as f:
        json.dump(data,f,indent=4)
def add_password(service,login,password):
    data = load_data()
    new_entry = {'service': service,'login': login,'password': password}
    data.append(new_entry)
    save_data(data)
def show_password():
    sp = load_data()
    if not sp:
        print('Password None')
    else:
        print('ALL PASSWORD')
        for x in sp:
            print(f'Service:{x['service']}\nLogin:{x['login']}\nPassword:{x['password']}')
def find_password(service:str):
    fd = load_data()
    for x in fd:
        if x['service'].lower() == service.lower():
            print(f'login:{x['login']}\nPassword:{x['password']}')
            return
    print("No service!")
def delete_password(service:str):
    df = load_data()
    for i,x in enumerate(df):
        if x['service'].lower() == service.lower():
            del df[i]
            save_data(df)
            print('Service delete')
            return
    print('No service!')
def main():
        while True:
            show_menu()
            try:
                choice = int(input('Enter num:'))
            except ValueError:
                print('ENTER NUM(1-7)')
                continue
            if choice == 1:
                service = input('enter service')
                login = input('enter login')
                password = input('enter password')
                add_password(service, login, password)
            elif choice == 2:
                show_password()
            elif choice == 3:
                service = input('enter name service:')
                find_password(service)
            elif choice == 4:
                service = input('enter name service:')
                delete_password(service)
            elif choice == 5:
                break
            else:
                print('Pls enter nums(1-5)')
main()

