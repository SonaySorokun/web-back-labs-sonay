from flask import Blueprint, render_template, request, redirect, session


lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/multiple-form')
def multiple_form():
    return render_template('lab4/multiple-form.html')


@lab4.route('/lab4/multiple', methods = ['POST'])
def multiple():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/multiple.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('lab4/exp-form.html')


@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/exp.html', error='Оба числа не могут быть нулями!')
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алекса Нейстат', 'gender': 'f'},
    {'login': 'bob', 'password': '64124', 'name': 'Боб Кварк', 'gender': 'm'},
    {'login': 'max', 'password': '457', 'name': 'Максим Батурин', 'gender': 'm'},
    {'login': 'anton', 'password': 'fghfgh', 'name': 'Антон Картавин', 'gender': 'm'},
    {'login': 'egor', 'password': 'weqweq', 'name': 'Егор Манилов', 'gender': 'm'},
    {'login': 'nikita', 'password': '999', 'name': 'Никита Саморуков', 'gender': 'm'},
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            current_login = session['login']
            user = next((u for u in users if u['login'] == current_login), None)
            if user:
                return render_template('lab4/login.html', authorized=True, login=user['login'], name=user['name'])
        
        return render_template('lab4/login.html', authorized=False, login='')

    login_value = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()

    if not login_value:
        return render_template('lab4/login.html', authorized=False, error='Не введён логин', login=login_value)
    
    if not password:
        return render_template('lab4/login.html', authorized=False, error='Не введён пароль', login=login_value)
    for user in users:
        if login_value == user['login'] and password == user['password']:
                session['login'] = login_value
                return render_template('lab4/login.html', authorized=True, login=login_value, name=user['name'], success='Успешная авторизация')

    return render_template('lab4/login.html', authorized=False, error='Неверные логин или пароль', login=login_value)
    
@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = None
    snowflakes = 0
    temp_value = ''

    if request.method == 'POST':
        temp = request.form.get('temperature')
        temp_value = temp

        if not temp:
            message = 'Ошибка: не задана температура'
        else:
            try:
                t = float(temp)

                if t < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif t > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= t <= -9:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 3
                elif -9 < t <= -5:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 2
                elif -5 < t <= -1:
                    message = f'Установлена температура: {t}°C'
                    snowflakes = 1
            except ValueError:
                message = 'Ошибка: температура должна быть числом'

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temp_value)