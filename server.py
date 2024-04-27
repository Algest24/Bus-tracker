from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('bus.db')


stops_data = [
    {
        "name": "3 мкр",
        "coordinates": [50.09688806533478, 45.423179677190774]
    },
    {
        "name": "ленина пятерочка",
        "coordinates": [50.10270773510453, 45.42261908377969]
    }
]

@app.route('/stops', methods=['GET'])
def get_stops():
    return jsonify({"stops": stops_data})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    # Подключение к базе данных
    db = get_db_connection()
    cursor = db.cursor()

    # Проверяем логин и пароль в базе данных
    cursor.execute("SELECT * FROM Drivers WHERE login=? AND password=?", (login, password))
    user = cursor.fetchone()

    if user:
        uid = user[0]
        db.close()  # Закрываем соединение с базой данных
        return jsonify({"uid": uid})
    else:
        db.close()  # Закрываем соединение с базой данных
        return jsonify({"error": "Неверный логин или пароль"}), 401

if __name__ == '__main__':
    app.run(debug=True)
