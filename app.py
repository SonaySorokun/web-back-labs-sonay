from flask import Flask, url_for, request
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
from db.models import users
from flask_login import LoginManager
from datetime import timedelta

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9


app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY', 'Секретно-секретный-секрет')
app.config['DB_TYPE']=os.getenv('DB_TYPE', 'postgres')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'sonya_sorokun_orm'
    db_user = 'sonya_sorokun_orm'
    db_password = '123a'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] =  \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "sonya_sorokun_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    
db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)


@app.route("/")
def title_page():
    lab1_url = url_for("lab1.lab")
    lab2_url = url_for("lab2.lab")
    lab3_url = url_for("lab3.lab")
    lab4_url = url_for("lab4.lab")
    lab5_url = url_for("lab5.lab")
    lab6_url = url_for("lab6.lab")
    lab7_url = url_for("lab7.lab")
    lab8_url = url_for("lab8.lab")
    lab8_url = url_for("lab9.lab")


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
                <li><a href="''' + lab4_url + '''">Лабораторная работа #4</a></li>
                <li><a href="''' + lab5_url + '''">Лабораторная работа #5</a></li>
                <li><a href="''' + lab6_url + '''">Лабораторная работа #6</a></li>
                <li><a href="''' + lab7_url + '''">Лабораторная работа #7</a></li>
                <li><a href="''' + lab8_url + '''">Лабораторная работа #8</a></li>
                <li><a href="''' + lab9_url + '''">Лабораторная работа #9</a></li>
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
