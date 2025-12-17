from flask import Blueprint, render_template, session, jsonify, request
import random
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

CONGRATULATIONS = [
    {"id": 1, "text": "С Новым годом! Желаю счастья!", "gift": "🎁"},
    {"id": 2, "text": "Пусть сбудутся все мечты!", "gift": "✨"},
    {"id": 3, "text": "Здоровья и удачи!", "gift": "🍀"},
    {"id": 4, "text": "Мира и добра!", "gift": "🕊️"},
    {"id": 5, "text": "Успехов в работе!", "gift": "💼"},
    {"id": 6, "text": "Любви и тепла!", "gift": "❤️"},
    {"id": 7, "text": "Процветания!", "gift": "💰", "requires_auth": True},
    {"id": 8, "text": "Весёлого праздника!", "gift": "🎉", "requires_auth": True},
    {"id": 9, "text": "Хорошего настроения!", "gift": "😊"},
    {"id": 10, "text": "Сладкой жизни!", "gift": "🍬"}
]

BOX_POSITIONS = [
    (10, 15), (30, 10), (50, 20), (70, 15), (85, 20),
    (15, 45), (35, 50), (55, 55), (75, 45), (65, 75)
]

def init_session():
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    if 'user' not in session:
        session['user'] = None

@lab9.route('/lab9/')
def lab():
    init_session()
    
    boxes = []
    for i in range(10):
        box = {
            'id': i + 1,
            'opened': i in session.get('opened_boxes', []),
            'position': BOX_POSITIONS[i],
            'requires_auth': CONGRATULATIONS[i].get('requires_auth', False)
        }
        boxes.append(box)
    
    opened_count = len(session.get('opened_boxes', []))
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         opened_count=opened_count,
                         user=session.get('user'))

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        
        if login_input and password:
            session['user'] = {
                'login': login_input,
                'name': login_input.capitalize()
            }
            return jsonify({'success': True})
    
    return render_template('lab9/login.html')

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        
        if login_input and password:
            session['user'] = {
                'login': login_input,
                'name': login_input.capitalize()
            }
            return jsonify({'success': True})
    
    return render_template('lab9/register.html')

@lab9.route('/lab9/logout')
def logout():
    session.pop('user', None)
    return jsonify({'success': True})

@lab9.route('/lab9/api/boxes')
def get_boxes_api():
    init_session()
    
    boxes_data = []
    for i in range(10):
        box = {
            'id': i + 1,
            'opened': i in session['opened_boxes'],
            'x': BOX_POSITIONS[i][0],
            'y': BOX_POSITIONS[i][1],
            'requires_auth': CONGRATULATIONS[i].get('requires_auth', False)
        }
        boxes_data.append(box)
    
    return jsonify(boxes_data)

@lab9.route('/lab9/api/open/<int:box_id>', methods=['POST'])
def open_box_api(box_id):
    init_session()
    
    if box_id < 1 or box_id > 10:
        return jsonify({'error': 'Нет такой коробки'}), 400
    
    opened_count = len(session.get('opened_boxes', []))
    if opened_count >= 3:
        return jsonify({'error': 'Можно открыть только 3 коробки'}), 400
    
    if (box_id - 1) in session.get('opened_boxes', []):
        return jsonify({'error': 'Коробка уже открыта'}), 400
    
    box_data = CONGRATULATIONS[box_id - 1]
    if box_data.get('requires_auth') and not session.get('user'):
        return jsonify({
            'error': 'Нужна авторизация',
            'requires_auth': True
        }), 403
    
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    session['opened_boxes'].append(box_id - 1)
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': box_data['text'],
        'gift': box_data['gift'],
        'opened_count': len(session['opened_boxes'])
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset_boxes():
    if not session.get('user'):
        return jsonify({'error': 'Нужна авторизация'}), 401
    
    session['opened_boxes'] = []
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'Дед Мороз {session["user"]["name"]} наполнил коробки!'
    })