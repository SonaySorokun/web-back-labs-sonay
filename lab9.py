from flask import Blueprint, render_template, session, jsonify, request
from flask_login import current_user

lab9 = Blueprint('lab9', __name__)

gifts = [
    {"id": 1, "image": "1.png", "congrat": "1.1.png"},
    {"id": 2, "image": "2.png", "congrat": "1.2.png"},
    {"id": 3, "image": "3.png", "congrat": "1.3.png"},
    {"id": 4, "image": "4.png", "congrat": "1.4.png"},
    {"id": 5, "image": "5.png", "congrat": "1.5.png"},
    {"id": 6, "image": "6.png", "congrat": "1.6.png"},
    {"id": 7, "image": "7.png", "congrat": "1.7.png", "lock": True},
    {"id": 8, "image": "8.png", "congrat": "1.8.png", "lock": True},
    {"id": 9, "image": "9.png", "congrat": "1.9.png"},
    {"id": 10, "image": "10.png", "congrat": "1.10.png"}
]

positions = [
    (10, 10), (30, 10), (50, 10), (70, 10), (90, 10),
    (10, 40), (30, 40), (50, 40), (70, 40), (90, 40)
]

@lab9.route('/lab9/')
def lab():
    if 'lab9_opened' not in session:
        session['lab9_opened'] = []
    
    boxes = []
    for i in range(10):
        boxes.append({
            'id': i+1,
            'opened': i in session['lab9_opened'],
            'x': positions[i][0],
            'y': positions[i][1],
            'lock': gifts[i].get('lock', False)
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
                         opened_count=len(session['lab9_opened']),
                         user_logged_in=user_logged_in,
                         user_name=user_name)

@lab9.route('/lab9/open/<int:box_id>')
def open_box(box_id):
    opened = session.get('lab9_opened', [])
    
    if len(opened) >= 3:
        return jsonify({'error': 'Лимит 3 коробки!'})
    
    if (box_id-1) in opened:
        return jsonify({'error': 'Уже открыта!'})
    
    if gifts[box_id-1].get('lock'):
        user_authenticated = False
        try:
            if current_user and current_user.is_authenticated:
                user_authenticated = True
        except:
            if 'user' not in session:
                user_authenticated = False
            else:
                user_authenticated = True
        
        if not user_authenticated:
            return jsonify({'error': 'Войдите для открытия!', 'lock': True})
    
    opened.append(box_id-1)
    session['lab9_opened'] = opened
    
    return jsonify({
        'ok': True,
        'congrat': gifts[box_id-1]['congrat'],
        'opened': len(opened)
    })

@lab9.route('/lab9/reset')
def reset():
    user_authenticated = False
    try:
        if current_user and current_user.is_authenticated:
            user_authenticated = True
    except:
        if 'user' not in session:
            user_authenticated = False
        else:
            user_authenticated = True
    
    if not user_authenticated:
        return jsonify({'error': 'Войдите для использования!'})
    
    session['lab9_opened'] = []
    return jsonify({'ok': True})