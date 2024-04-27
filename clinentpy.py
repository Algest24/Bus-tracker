import requests

def login():
    url = 'http://127.0.0.1:5000/login'
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    data = {'login': login, 'password': password}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("UID:", response.json()['uid'])
    else:
        print("Ошибка:", response.json()['error'])

if __name__ == '__main__':
    login()
