from flask import Blueprint, render_template, session, jsonify, request

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
    if 'opened' not in session:
        session['opened'] = []
    
    boxes = []
    for i in range(10):
        boxes.append({
            'id': i+1,
            'opened': i in session['opened'],
            'x': positions[i][0],
            'y': positions[i][1],
            'lock': gifts[i].get('lock', False)
        })
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         opened_count=len(session['opened']))

@lab9.route('/lab9/open/<int:box_id>')
def open_box(box_id):
    opened = session.get('opened', [])
    
    if len(opened) >= 3:
        return jsonify({'error': 'Лимит 3 коробки!'})
    
    if (box_id-1) in opened:
        return jsonify({'error': 'Уже открыта!'})
    
    if gifts[box_id-1].get('lock') and 'user' not in session:
        return jsonify({'error': 'Нужен вход!', 'lock': True})
    
    opened.append(box_id-1)
    session['opened'] = opened
    
    return jsonify({
        'ok': True,
        'congrat': gifts[box_id-1]['congrat'],
        'opened': len(opened)
    })

@lab9.route('/lab9/login', methods=['POST'])
def login():
    login = request.form.get('login')
    if login:
        session['user'] = login
        return jsonify({'ok': True})
    return jsonify({'error': 'Введите логин'})

@lab9.route('/lab9/logout')
def logout():
    session.pop('user', None)
    return jsonify({'ok': True})

@lab9.route('/lab9/reset')
def reset():
    if 'user' not in session:
        return jsonify({'error': 'Нужен вход!'})
    
    session['opened'] = []
    return jsonify({'ok': True})