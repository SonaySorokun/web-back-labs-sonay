from flask import Flask, url_for, request
from datetime import datetime

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


@app.route("/")
def title_page():
    lab1_url = url_for("lab1.lab")
    lab2_url = url_for("lab2.lab")
    lab3_url = url_for("lab3.lab")


    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <hr>
    </header>
    <main>
        <div class="menu"> 
            <ul>
                <li><a href="''' + lab1_url + '''">Лабораторная работа #1</a></li>
                <li><a href="''' + lab2_url + '''">Лабораторная работа #2</a></li>
                <li><a href="''' + lab3_url + '''">Лабораторная работа #3</a></li>
            </ul>
        </div>
    </main>
    <footer>
        <hr>
        &copy;Сорокун Соня, ФБИ-32, 3 курс, 2025
    </footer>
</body>
</html>
'''

access_log = []

@app.errorhandler(404)
def not_found(err):
    client_ip = request.remote_addr
    access_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    root_url = url_for('title_page')

    log_entry = {
        'ip': client_ip,
        'date': access_date,
        'url': requested_url
    }
    access_log.append(log_entry)
    
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка 404</title>
    <style>
        h1, h2 {
            font-size: 200px;
            color: violet;
            text-shadow: 5px 5px 10px purple;
            text-align: center;
            margin-bottom: 0;
            margin-top: 60px;
            animation: float 3s ease-in-out infinite;
        }

        h2 {
            font-size: 40px;
            text-shadow: none;
        }
        
        .info {
            background-color: #f0f0f0;
            padding: 20px;
            margin: 20px;
            border-radius: 10px;
        }
        
        .log {
            background-color: #e0e0e0;
            padding: 15px;
            margin: 20px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 14px;
        }
    
        @keyframes float {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
        }

    </style>
</head>
<body>
    <main>
        <h1>404</h1>
        <h2>Страница по запрашиваемому адресу не найдена</h2>
        
        <div class="info">
            <h3>Информация о запросе:</h3>
            <p><strong>IP-адрес пользователя:</strong> ''' + client_ip + '''</p>
            <p><strong>Дата и время доступа:</strong> ''' + access_date + '''</p>
            <p><strong>Запрошенный URL:</strong> ''' + requested_url + '''</p>
            <p><a href="''' + root_url + '''">Вернуться на главную страницу</a></p>
        </div>
        
        <div class="log">
            <h3>Полный лог посещений (404 ошибки):</h3>
            <ul>
''' + '\n'.join([f'<li>{entry["date"]} - IP: {entry["ip"]} - URL: {entry["url"]}</li>' for entry in access_log]) + '''
            </ul>
        </div>
    </main>
</body>
</html>
''', 404

@app.errorhandler(500)
def internal_error(err):
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ошибка 500</title>
    <style>
        h1, h2 {
            font-size: 200px;
            color: grey;
            text-shadow: 5px 5px 10px black;
            text-align: center;
            margin-bottom: 0;
            margin-top: 60px;
        }

         h2 {
            font-size: 40px;
            text-shadow: none;
        }

    </style>
</head>
<body>
    <main>
        <h1>500</h1>
        <h2>Внутренняя ошибка сервера</h2>
    </main>
</body>
</html>
''', 500
