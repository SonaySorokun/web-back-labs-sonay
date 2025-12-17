from flask import Blueprint, render_template, request, jsonify, session
import random

lab9 = Blueprint('lab9', __name__)

CONGRATULATIONS = [
    "С Новым годом!",
    "Желаю счастья!",
    "Пусть сбудутся мечты!",
    "Удачи и успехов!",
    "Здоровья и радости!",
    "Мира и добра!",
    "Процветания!",
    "Любви и тепла!",
    "Уюта в доме!",
    "Хорошего настроения!"
]

def init_session():
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    if 'box_positions' not in session:
        positions = []
        for _ in range(10):
            positions.append({
                'x': random.randint(10, 85),
                'y': random.randint(10, 85)
            })
        session['box_positions'] = positions

@lab9.route('/lab9/')
def main():
    init_session()
    return render_template('lab9/index.html')

@lab9.route('/lab9/get_boxes')
def get_boxes():
    init_session()
    
    boxes = []
    for i in range(10):
        boxes.append({
            'id': i,
            'x': session['box_positions'][i]['x'],
            'y': session['box_positions'][i]['y'],
            'opened': i in session.get('opened_boxes', [])
        })
    
    opened_count = len(session.get('opened_boxes', []))
    
    return jsonify({
        'boxes': boxes,
        'opened': opened_count,
        'remaining': 10 - opened_count
    })

@lab9.route('/lab9/open/<int:box_id>')
def open_box(box_id):
    init_session()
    
    opened = session.get('opened_boxes', [])
    if len(opened) >= 3:
        return jsonify({'error': 'Можно открыть только 3 коробки'})
    
    if box_id in opened:
        return jsonify({'error': 'Коробка уже открыта'})
    
    # Открываем
    opened.append(box_id)
    session['opened_boxes'] = opened
    
    return jsonify({
        'success': True,
        'text': CONGRATULATIONS[box_id],
        'opened': len(opened),
        'remaining': 10 - len(opened)
    })

@lab9.route('/lab9/reset')
def reset():
    session.pop('opened_boxes', None)
    session.pop('box_positions', None)
    return jsonify({'success': True})