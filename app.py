from flask import Flask, url_for, request, redirect, abort
from datetime import datetime
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Глобальный список для хранения лога посещений
access_log = []

@app.route("/")
@app.route("/index")
def title_page():
    lab1 = url_for("lab1")

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
                <li><a href="''' + lab1 + '''">Первая лабораторная</a></li>
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

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask </h1>
               <a href="/lab1/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/")
def lab1():
    main_menu = url_for('title_page')
    web_url = url_for('web')
    author_url = url_for('author')
    image_url = url_for('image')
    counter_url = url_for('counter')
    clear_counter_url = url_for('clear_counter')
    info_url = url_for('info')
    created_url = url_for('created')
    error_400_url = url_for('error_400')
    error_401_url = url_for('error_401')
    error_402_url = url_for('error_402')
    error_403_url = url_for('error_403')
    error_405_url = url_for('error_405')
    error_418_url = url_for('error_418')
    error_500_url = url_for('error_500')

    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Лабораторная 1</title>
</head>
<body>
    <main>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.</p>

        <br><a href="''' + main_menu + '''">Назад в главное меню</a>

        <h2>Список роутов</h2>

        <ul>
            <li><a href="''' + web_url + '''">/lab1/web</a></li>
            <li><a href="''' + author_url + '''">/lab1/author</a></li>
            <li><a href="''' + image_url + '''">/lab1/image</a></li>
            <li><a href="''' + counter_url + '''">/lab1/counter</a></li>
            <li><a href="''' + clear_counter_url + '''">/lab1/counter/clear</a></li>
            <li><a href="''' + info_url + '''">/lab1/info</a></li>
            <li><a href="''' + created_url + '''">/lab1/create</a></li>
            <li><a href="''' + error_400_url + '''">/lab1/400</a></li>
            <li><a href="''' + error_401_url + '''">/lab1/401</a></li>
            <li><a href="''' + error_402_url + '''">/lab1/402</a></li>
            <li><a href="''' + error_403_url + '''">/lab1/403</a></li>
            <li><a href="''' + error_405_url + '''">/lab1/405</a></li>
            <li><a href="''' + error_418_url + '''">/lab1/418</a></li>
            <li><a href="''' + error_500_url + '''">/lab1/500</a></li>
            <li><a href="/lab1/aboba">Несуществующая страница</a></li>
        </ul>
    </main>
</body>
</html>
'''

@app.route("/lab1/author")
def author():
    name = "Сорокун Соня Романовна"
    group = "ФБИ-32"
    faculty = "ФБ"
    lab1_url = url_for('lab1')

    return"""<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href=""" + lab1_url + """>Назад к лабе 1</a>
           </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename = "oak.jpg")
    style = url_for("static", filename = "lab1.css")
    lab1_url = url_for('lab1')

    return'''<!doctype html>
        <html>
           <head>
               <link rel="stylesheet" href="''' + style + '''">
           </head>
           <body>
               <h1>Дуб</h1>
               <img src="''' + path + '''">
               <br><a href="''' + lab1_url + '''">Назад к лабе 1</a>
           </body>
        </html>''', 200, {
            'Content-Language': 'ru',
            'X-Img-Name': 'oak',
            'X-Hotel': 'Trivago'
        }

count = 0

@app.route("/lab1/counter")
def counter():
    global count    
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr
    counter_clear_route = url_for('clear_counter')
    lab1_url = url_for('lab1')

    count += 1
    return'''
<!doctype html>
    <html>
        <body>
            Сколько раз вы сюда заходили: ''' + str(count) + '''
            <hr>
            Дата и время: ''' + str(time) + '''
            <br> Запрошенный адрес: ''' + url + '''
            <br> Ваш IP адрес: ''' + client_ip + '''
            <br><a href="''' + counter_clear_route + '''">Обнулить счетчик</a>
            <br><a href="''' + lab1_url + '''">Назад к лабе 1</a>
        </body>
    </html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/counter/clear")
def clear_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/create")
def created():
    lab1_url = url_for('lab1')
    return'''
<!doctype html>
    <html>
        <body>
            <h1>Создано успешно!</h1>
            <div><i>Что-то создано...</i></div>
            <br><a href="''' + lab1_url + '''">Назад к лабе 1</a>
        </body>
    </html>
''', 201

@app.route("/lab1/400")
def error_400():
    return "Некорректный запрос", 400

@app.route("/lab1/401")
def error_401():
    return "Пользователь не авторизован", 401

@app.route("/lab1/402")
def error_402():
    return "Необходима оплата", 402

@app.route("/lab1/403")
def error_403():
    return "Доступ закрыт", 403

@app.route("/lab1/405")
def error_405():
    return "Метод не поддерживается", 405

@app.route("/lab1/418")
def error_418():
    return "Я чайник :D", 418

@app.route("/lab1/500")
def error_500():
    abort(500)

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


@app.route('/lab2/a/')
def a_slash():
    return 'ok'

@app.route('/lab2/a')
def a():
    return 'ok'

flower_list = ['роза','тюльпан','незабудка','ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id > len(flower_list):
        abort(404)
    else:
        return f'Цветок: {flower_list[flower_id]}'

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
    </body>
</html>    
'''