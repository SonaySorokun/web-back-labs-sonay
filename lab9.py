from flask import Blueprint, render_template, session, jsonify, request
from flask_login import current_user
import json
import os

lab9 = Blueprint('lab9', __name__)

gifts = [
    {"id": 1, "image": "1.png", "congrat": "1.1.png", 
     "text": "С Новым годом! Пусть сбудутся все мечты!", "lock": False},
    {"id": 2, "image": "2.png", "congrat": "1.2.png", 
     "text": "Желаю здоровья, счастья и удачи!", "lock": False},
    {"id": 3, "image": "3.png", "congrat": "1.3.png", 
     "text": "Пусть новый год принесёт много радости!", "lock": False},
    {"id": 4, "image": "4.png", "congrat": "1.4.png", 
     "text": "Успехов в работе и личной жизни!", "lock": False},
    {"id": 5, "image": "5.png", "congrat": "1.5.png", 
     "text": "Мира, добра и тепла в доме!", "lock": False},
    {"id": 6, "image": "6.png", "congrat": "1.6.png", 
     "text": "Процветания и финансового благополучия!", "lock": False},
    {"id": 7, "image": "7.png", "congrat": "1.7.png", 
     "text": "Любви, которая согреет самые холодные дни!", "lock": True},
    {"id": 8, "image": "8.png", "congrat": "1.8.png", 
     "text": "Весёлых праздников и отличного настроения!", "lock": True},
    {"id": 9, "image": "9.png", "congrat": "1.9.png", 
     "text": "Крепкого здоровья на весь год!", "lock": False},
    {"id": 10, "image": "10.png", "congrat": "1.10.png", 
     "text": "Исполнения самых заветных желаний!", "lock": False}
]

positions = [
    (10, 10), (30, 10), (50, 10), (70, 10), (90, 10),
    (10, 40), (30, 40), (50, 40), (70, 40), (90, 40)
]

def get_user_id():
    # Для авторизованных пользователей
    try:
        if current_user and current_user.is_authenticated:
            if 'lab9_user_id' not in session:
                session['lab9_user_id'] = f"user_{current_user.id}"
            return session['lab9_user_id']
    except:
        pass
    
    # Для гостей
    if 'lab9_user_id' not in session:
        session['lab9_user_id'] = f"guest_{os.urandom(8).hex()}"
    return session['lab9_user_id']

@lab9.route('/lab9/')
def lab():
    user_id = get_user_id()
    
    if 'lab9_data' not in session:
        session['lab9_data'] = {}
    
    if user_id not in session['lab9_data']:
        session['lab9_data'][user_id] = {
            'opened': [],
            'count': 0
        }
    
    boxes = []
    user_data = session['lab9_data'][user_id]
    
    for i in range(10):
        boxes.append({
            'id': i+1,
            'opened': i in user_data['opened'],
            'x': positions[i][0],
            'y': positions[i][1],
            'lock': gifts[i]['lock']
        })
    
    user_logged_in = False
    user_name = None
    
    try:
        if current_user and current_user.is_authenticated:
            user_logged_in = True
            user_name = getattr(current_user, 'login', 'Пользователь')
    except:
        if 'user' in session:
            user_logged_in = True
            user_name = session.get('user')
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         opened_count=user_data['count'],
                         user_logged_in=user_logged_in,
                         user_name=user_name)

@lab9.route('/lab9/open/<int:box_id>')
def open_box(box_id):
    user_id = get_user_id()
    
    if 'lab9_data' not in session or user_id not in session['lab9_data']:
        return jsonify({'error': 'Ошибка данных'})
    
    user_data = session['lab9_data'][user_id]
    
    if user_data['count'] >= 3:
        return jsonify({'error': f'Вы уже открыли {user_data["count"]} коробок. Лимит 3!'})
    
    if (box_id-1) in user_data['opened']:
        return jsonify({'error': 'Эта коробка уже открыта!'})
    
    if gifts[box_id-1]['lock']:
        try:
            if not (current_user and current_user.is_authenticated):
                return jsonify({'error': 'Войдите для открытия этой коробки!', 'lock': True})
        except:
            if 'user' not in session:
                return jsonify({'error': 'Войдите для открытия этой коробки!', 'lock': True})
    
    user_data['opened'].append(box_id-1)
    user_data['count'] = len(user_data['opened'])
    session['lab9_data'][user_id] = user_data
    session.modified = True
    
    return jsonify({
        'ok': True,
        'congrat': gifts[box_id-1]['congrat'],
        'text': gifts[box_id-1]['text'],
        'count': user_data['count']
    })

@lab9.route('/lab9/reset')
def reset():
    try:
        if not (current_user and current_user.is_authenticated):
            return jsonify({'error': 'Войдите для использования этой функции!'})
    except:
        if 'user' not in session:
            return jsonify({'error': 'Войдите для использования этой функции!'})
    
    user_id = get_user_id()
    
    if 'lab9_data' in session and user_id in session['lab9_data']:
        session['lab9_data'][user_id] = {
            'opened': [],
            'count': 0
        }
        session.modified = True
    
    return jsonify({'ok': True})

@lab9.route('/lab9/logout')
def logout():
    session.pop('lab9_data', None)
    return jsonify({'ok': True})