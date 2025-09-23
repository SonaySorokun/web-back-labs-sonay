from flask import Flask, url_for, request, redirect, abort
from datetime import datetime
from werkzeug.exceptions import HTTPException
app = Flask(__name__)

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

@app.route("/lab1/")
@app.route("/lab1/web")
def lab1():

    main_menu = url_for('title_page')

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
    </main>
</body>
</html>
'''

@app.route("/lab1/author")
def author():
    name = "Сорокун Соня Романовна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return("""<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/web">web</a>
           </body>
        </html>""")

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
            <br><a href="''' +  counter_clear_route + '''">Обнулить счетчик</a>
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
    return'''
<!doctype html>
    <html>
        <body>
            <h1>Создано успешно!</h1>
            <div><i>Что-то создано...</i></div>
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

    a = 0
    b = 100

    return b/a

@app.errorhandler(404)
def not_found(err):

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
    </main>
</body>
</html>
'''

@app.errorhandler(500)
def not_found(err):
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
'''