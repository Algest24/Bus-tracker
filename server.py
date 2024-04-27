from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Подключение к базе данных
db = sqlite3.connect('bus.db')
cursor = db.cursor()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    # Проверяем логин и пароль в базе данных
    cursor.execute("SELECT * FROM Drivers WHERE login=? AND password=?", (login, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"uid": user[0]})
    else:
        return jsonify({"error": "Неверный логин или пароль"}), 401

if __name__ == '__main__':
    app.run(debug=True)
