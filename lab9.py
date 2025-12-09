from flask import Blueprint, render_template, request, jsonify, session
import json
import random
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

# Новогодние поздравления
CONGRATULATIONS = [
    {
        "id": 1,
        "text": "🎄 С Новым годом! Пусть сбудутся все твои мечты!",
        "gift": "/static/lab9/gift1.png",
        "gift_name": "Золотая ёлочная игрушка"
    },
    {
        "id": 2,
        "text": "❄️ Желаю здоровья, счастья и удачи в новом году!",
        "gift": "/static/lab9/gift2.png",
        "gift_name": "Снежный шар"
    },
    {
        "id": 3,
        "text": "🌟 Пусть новый год принесёт много радостных моментов!",
        "gift": "/static/lab9/gift3.png",
        "gift_name": "Сияющая звезда"
    },
    {
        "id": 4,
        "text": "🎁 Желаю, чтобы каждый день нового года был наполнен счастьем!",
        "gift": "/static/lab9/gift4.png",
        "gift_name": "Подарочный набор"
    },
    {
        "id": 5,
        "text": "🦌 Пусть ангел-хранитель всегда будет рядом с тобой!",
        "gift": "/static/lab9/gift5.png",
        "gift_name": "Фигурка оленя"
    },
    {
        "id": 6,
        "text": "✨ С новым годом! Пусть всё хорошее приумножится!",
        "gift": "/static/lab9/gift6.png",
        "gift_name": "Блестящий фейерверк"
    },
    {
        "id": 7,
        "text": "🎅 Желаю исполнения самых заветных желаний!",
        "gift": "/static/lab9/gift7.png",
        "gift_name": "Шапка Деда Мороза"
    },
    {
        "id": 8,
        "text": "🕯️ Пусть новый год будет волшебным и тёплым!",
        "gift": "/static/lab9/gift8.png",
        "gift_name": "Новогодняя свеча"
    },
    {
        "id": 9,
        "text": "🍪 Пусть в вашем доме всегда пахнет мандаринами и ёлкой!",
        "gift": "/static/lab9/gift9.png",
        "gift_name": "Пряничный домик"
    },
    {
        "id": 10,
        "text": "🎊 Пусть новый год принесёт мир, любовь и благополучие!",
        "gift": "/static/lab9/gift10.png",
        "gift_name": "Праздничный серпантин"
    }
]

def init_gifts():
    """Инициализация позиций коробок"""
    if 'lab9_gifts' not in session:
        # Генерируем случайные позиции, но фиксированные для сессии
        random.seed(session.get('lab9_seed', str(datetime.now().timestamp())))
        session['lab9_seed'] = str(datetime.now().timestamp())
        
        positions = []
        for i in range(10):
            # Генерация уникальных позиций
            while True:
                x = random.randint(5, 85)
                y = random.randint(15, 80)
                
                # Проверка на минимальное расстояние между коробками
                too_close = False
                for pos in positions:
                    distance = ((pos['x'] - x) ** 2 + (pos['y'] - y) ** 2) ** 0.5
                    if distance < 15:  # Минимальное расстояние 15%
                        too_close = True
                        break
                
                if not too_close:
                    break
            
            positions.append({
                'id': i,
                'x': x,
                'y': y,
                'opened': False,
                'congrat_id': i
            })
        
        session['lab9_gifts'] = positions
        session['lab9_opened_count'] = 0

@lab9.route('/lab9/')
def lab():
    """Главная страница лабораторной"""
    init_gifts()
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/api/gifts')
def get_gifts():
    """Получение информации о коробках"""
    init_gifts()
    gifts = session.get('lab9_gifts', [])
    opened_count = session.get('lab9_opened_count', 0)
    
    return jsonify({
        'success': True,
        'gifts': gifts,
        'opened_count': opened_count,
        'remaining': 10 - opened_count,
        'max_opens': 3
    })

@lab9.route('/lab9/api/open/<int:gift_id>', methods=['POST'])
def open_gift(gift_id):
    """Открытие коробки"""
    if 'lab9_opened_count' not in session:
        session['lab9_opened_count'] = 0
    
    # Проверка лимита открытий
    if session['lab9_opened_count'] >= 3:
        return jsonify({
            'success': False,
            'message': '🎅 Вы уже открыли максимальное количество коробок (3)!'
        }), 400
    
    gifts = session.get('lab9_gifts', [])
    
    # Поиск коробки
    gift = next((g for g in gifts if g['id'] == gift_id), None)
    
    if not gift:
        return jsonify({'success': False, 'message': 'Коробка не найдена'}), 404
    
    if gift['opened']:
        return jsonify({
            'success': False, 
            'message': '🎁 Эта коробка уже открыта!'
        }), 400
    
    # Открываем коробку
    gift['opened'] = True
    session['lab9_opened_count'] += 1
    session['lab9_gifts'] = gifts
    
    # Получаем поздравление
    congrat = CONGRATULATIONS[gift_id]
    
    return jsonify({
        'success': True,
        'congratulation': congrat['text'],
        'gift_image': congrat['gift'],
        'gift_name': congrat['gift_name'],
        'opened_count': session['lab9_opened_count'],
        'remaining': 10 - session['lab9_opened_count']
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset():
    """Сброс прогресса"""
    session.pop('lab9_gifts', None)
    session.pop('lab9_opened_count', None)
    session.pop('lab9_seed', None)
    return jsonify({'success': True})