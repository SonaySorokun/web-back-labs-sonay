from flask import Blueprint, render_template, session, jsonify, request, url_for
import random

lab9 = Blueprint('lab9', __name__)

GIFTS = [
    {
        "id": 1,
        "gift_image": "1.png",
        "congrat_image": "1.1.png",
        "title": "Золотая ёлочка"
    },
    {
        "id": 2,
        "gift_image": "2.png",
        "congrat_image": "1.2.png",
        "title": "Волшебный снеговик"
    },
    {
        "id": 3,
        "gift_image": "3.png",
        "congrat_image": "1.3.png",
        "title": "Кристалл удачи"
    },
    {
        "id": 4,
        "gift_image": "4.png",
        "congrat_image": "1.4.png",
        "title": "Мандарин счастья"
    },
    {
        "id": 5,
        "gift_image": "5.png",
        "congrat_image": "1.5.png",
        "title": "Сердечко тепла"
    },
    {
        "id": 6,
        "gift_image": "6.png",
        "congrat_image": "1.6.png",
        "title": "Солнечный зайчик"
    },
    {
        "id": 7,
        "gift_image": "7.png",
        "congrat_image": "1.7.png",
        "title": "Кубок победителя",
        "requires_auth": True
    },
    {
        "id": 8,
        "gift_image": "8.png",
        "congrat_image": "1.8.png",
        "title": "Четырехлистный клевер",
        "requires_auth": True
    },
    {
        "id": 9,
        "gift_image": "9.png",
        "congrat_image": "1.9.png",
        "title": "Домик мечты"
    },
    {
        "id": 10,
        "gift_image": "10.png",
        "congrat_image": "1.10.png",
        "title": "Волшебная звезда"
    }
]

BOX_POSITIONS = [
    (15, 20), (35, 15), (55, 25), (75, 20), (20, 50),
    (40, 55), (60, 60), (80, 50), (30, 80), (65, 85)
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
        boxes.append({
            'id': i + 1,
            'opened': i in session.get('opened_boxes', []),
            'position': BOX_POSITIONS[i],
            'requires_auth': GIFTS[i].get('requires_auth', False),
            'gift_image': GIFTS[i]['gift_image'],
            'title': GIFTS[i]['title']
        })
    
    opened_count = len(session.get('opened_boxes', []))
    
    return render_template('lab9/index.html', 
                         boxes=boxes,
                         opened_count=opened_count,
                         user=session.get('user'),
                         static_url=url_for('static', filename=''))

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
            session.modified = True
            return jsonify({'success': True})
        
        return jsonify({'error': 'Заполните все поля'}), 400
    
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
            session.modified = True
            return jsonify({'success': True})
        
        return jsonify({'error': 'Заполните все поля'}), 400
    
    return render_template('lab9/register.html')

@lab9.route('/lab9/logout')
def logout():
    session.pop('user', None)
    session.modified = True
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
            'requires_auth': GIFTS[i].get('requires_auth', False),
            'gift_image': GIFTS[i]['gift_image'],
            'title': GIFTS[i]['title']
        }
        boxes_data.append(box)
    
    return jsonify({
        'boxes': boxes_data,
        'opened_count': len(session['opened_boxes']),
        'user': session.get('user'),
        'static_url': url_for('static', filename='')
    })

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
    
    gift_data = GIFTS[box_id - 1]
    if gift_data.get('requires_auth') and not session.get('user'):
        return jsonify({
            'error': 'Для открытия этой коробки нужно войти в систему',
            'requires_auth': True
        }), 403
    
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    session['opened_boxes'].append(box_id - 1)
    session.modified = True
    
    return jsonify({
        'success': True,
        'congrat_image': gift_data['congrat_image'],
        'title': gift_data['title'],
        'opened_count': len(session['opened_boxes']),
        'static_url': url_for('static', filename='')
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset_boxes():
    if not session.get('user'):
        return jsonify({'error': 'Только авторизованные пользователи могут вызывать Деда Мороза'}), 401
    
    session['opened_boxes'] = []
    session.modified = True
    
    return jsonify({
        'success': True,
        'message': f'🎅 Дед Мороз {session["user"]["name"]} наполнил все коробки заново!'
    })