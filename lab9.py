import json
import random
from flask import Blueprint, render_template, request, jsonify, session

lab9 = Blueprint('lab9', __name__, template_folder='templates')

# Новогодние поздравления - КАЖДОМУ ID СООТВЕТСТВУЕТ СВОЕ ПОЗДРАВЛЕНИЕ И КАРТИНКА
CONGRATULATIONS = [
    {
        "id": 0,
        "text": "Пусть Новый год принесёт много радости, счастья и удачи! Желаем исполнения всех желаний и ярких впечатлений!",
        "gift_name": "Золотой колокольчик",
        "image": "gift1.png"
    },
    {
        "id": 1,
        "text": "С Новым годом! Пусть ангел-хранитель оберегает вас, а Дед Мороз исполнит самые заветные мечты!",
        "gift_name": "Волшебный шар",
        "image": "gift2.png"
    },
    {
        "id": 2,
        "text": "Желаем, чтобы новый год был наполнен уютом, теплом семейного очага и приятными сюрпризами!",
        "gift_name": "Тёплый плед",
        "image": "gift3.png"
    },
    {
        "id": 3,
        "text": "Пусть каждый день нового года будет похож на сказку, полную чудес, волшебства и добрых встреч!",
        "gift_name": "Книга сказок",
        "image": "gift4.png"
    },
    {
        "id": 4,
        "text": "С новым годом! Желаем крепкого здоровья, финансового благополучия и карьерного роста!",
        "gift_name": "Золотой ключ",
        "image": "gift5.png"
    },
    {
        "id": 5,
        "text": "Пусть новый год подарит море улыбок, верных друзей и незабываемых путешествий!",
        "gift_name": "Чемодан мечты",
        "image": "gift6.png"
    },
    {
        "id": 6,
        "text": "Желаем, чтобы снегопад удачи сыпался на вас весь год, а каждый день приносил новые победы!",
        "gift_name": "Снежный глобус",
        "image": "gift7.png"
    },
    {
        "id": 7,
        "text": "С Новым годом! Пусть ваша ёлка будет самой красивой, а праздник — самым весёлым!",
        "gift_name": "Ёлочная игрушка",
        "image": "gift8.png"
    },
    {
        "id": 8,
        "text": "Желаем найти свою золотую жилу в новом году! Пусть удача всегда будет на вашей стороне!",
        "gift_name": "Сундук с сокровищами",
        "image": "gift9.png"
    },
    {
        "id": 9,
        "text": "Пусть новый год станет годом великих открытий, творческих успехов и личных достижений!",
        "gift_name": "Карта мира",
        "image": "gift10.png"
    }
]

# Картинки коробок на поле - каждая соответствует своему поздравлению
GIFT_BOX_IMAGES = [
    "/static/lab9/gifts/gift_box1.png",  # для congrat id=0
    "/static/lab9/gifts/gift_box2.png",  # для congrat id=1
    "/static/lab9/gifts/gift_box3.png",  # для congrat id=2
    "/static/lab9/gifts/gift_box4.png",  # для congrat id=3
    "/static/lab9/gifts/gift_box5.png",  # для congrat id=4
    "/static/lab9/gifts/gift_box6.png",  # для congrat id=5
    "/static/lab9/gifts/gift_box7.png",  # для congrat id=6
    "/static/lab9/gifts/gift_box8.png",  # для congrat id=7
    "/static/lab9/gifts/gift_box9.png",  # для congrat id=8
    "/static/lab9/gifts/gift_box10.png"  # для congrat id=9
]

# Хранилище состояний (в памяти)
gift_states = {}

def generate_gift_positions():
    """Генерация позиций в предопределенных зонах"""
    zones = [
        {"min_top": 5, "max_top": 25, "min_left": 2, "max_left": 20},
        {"min_top": 5, "max_top": 25, "min_left": 25, "max_left": 45},
        {"min_top": 5, "max_top": 25, "min_left": 50, "max_left": 70},
        {"min_top": 5, "max_top": 25, "min_left": 75, "max_left": 90},
        {"min_top": 30, "max_top": 50, "min_left": 2, "max_left": 20},
        {"min_top": 30, "max_top": 50, "min_left": 25, "max_left": 45},
        {"min_top": 30, "max_top": 50, "min_left": 50, "max_left": 70},
        {"min_top": 30, "max_top": 50, "min_left": 75, "max_left": 90},
        {"min_top": 55, "max_top": 75, "min_left": 10, "max_left": 30},
        {"min_top": 55, "max_top": 75, "min_left": 65, "max_left": 85},
    ]
    
    positions = []
    
    # Создаем список всех ID подарков (0-9)
    all_gift_ids = list(range(10))
    
    # Перемешиваем ID подарков - каждый подарок получает случайную позицию
    random.shuffle(all_gift_ids)
    
    # Перемешиваем зоны
    shuffled_zones = random.sample(zones, len(zones))
    
    for i in range(10):
        zone = shuffled_zones[i]
        gift_id = all_gift_ids[i]  # Перемешанный ID подарка
        
        top = random.randint(zone["min_top"], zone["max_top"])
        left = random.randint(zone["min_left"], zone["max_left"])
        
        positions.append({
            "id": gift_id,  # ID подарка (0-9)
            "top": f"{top}%",
            "left": f"{left}%",
            "opened": False,
            "box_image": GIFT_BOX_IMAGES[gift_id]  # Картинка коробки, соответствующая ID
        })
    
    return positions

@lab9.route('/lab9')
def lab9_route():
    """Главная страница лабораторной работы 9"""
    # Инициализация сессии
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}_{random.randint(1000, 9999)}"
        session['opened_count'] = 0
    
    user_id = session['user_id']
    
    # Инициализируем состояния для пользователя
    if user_id not in gift_states:
        gift_states[user_id] = {
            "positions": generate_gift_positions(),
            "opened_gifts": [],
            "congratulations": CONGRATULATIONS  # НЕ перемешиваем!
        }
    
    # Подсчитываем статистику
    opened_count = session.get('opened_count', 0)
    total_opened = len(gift_states[user_id]['opened_gifts'])
    remaining = 10 - total_opened
    
    return render_template('lab9/lab9.html',
                         opened_count=opened_count,
                         remaining_count=remaining,
                         user_id=user_id)

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    """Обработка открытия подарка"""
    try:
        data = request.get_json()
        gift_id = data.get('gift_id')
        
        # Проверяем корректность ID подарка
        if not isinstance(gift_id, int) or gift_id < 0 or gift_id >= 10:
            return jsonify({"success": False, "error": "Неверный ID подарка"})
        
        user_id = session.get('user_id')
        if not user_id or user_id not in gift_states:
            return jsonify({"success": False, "error": "Сессия не найдена"})
        
        user_state = gift_states[user_id]
        
        # Проверяем, не открыт ли уже подарок
        if gift_id in user_state['opened_gifts']:
            return jsonify({
                "success": False, 
                "error": "Этот подарок уже открыт",
                "already_opened": True
            })
        
        # Проверяем лимит открытых подарков
        opened_count = session.get('opened_count', 0)
        if opened_count >= 3:
            return jsonify({
                "success": False,
                "error": "Вы уже открыли максимальное количество подарков (3)",
                "limit_reached": True
            })
        
        # Открываем подарок
        user_state['opened_gifts'].append(gift_id)
        session['opened_count'] = opened_count + 1
        
        # Получаем поздравление по ID
        congrat = None
        for c in user_state['congratulations']:
            if c['id'] == gift_id:
                congrat = c
                break
        
        if not congrat:
            # Если вдруг не нашли, берем по индексу
            congrat = CONGRATULATIONS[gift_id]
        
        # Обновляем состояние позиции
        for pos in user_state['positions']:
            if pos['id'] == gift_id:
                pos['opened'] = True
                break
        
        return jsonify({
            "success": True,
            "congratulation": congrat,
            "opened_count": session['opened_count'],
            "remaining_count": 10 - len(user_state['opened_gifts'])
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/reset', methods=['POST'])
def reset_game():
    """Сброс игры"""
    try:
        user_id = session.get('user_id')
        if user_id in gift_states:
            # Генерируем новые позиции
            gift_states[user_id] = {
                "positions": generate_gift_positions(),
                "opened_gifts": [],
                "congratulations": CONGRATULATIONS
            }
        
        # Сбрасываем счетчик открытых подарков
        session['opened_count'] = 0
        
        return jsonify({
            "success": True,
            "message": "Игра сброшена",
            "opened_count": 0,
            "remaining_count": 10
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/get_state', methods=['GET'])
def get_state():
    """Получение текущего состояния игры"""
    try:
        user_id = session.get('user_id')
        if not user_id or user_id not in gift_states:
            return jsonify({"success": False, "error": "Сессия не найдена"})
        
        user_state = gift_states[user_id]
        
        return jsonify({
            "success": True,
            "positions": user_state['positions'],
            "opened_gifts": user_state['opened_gifts'],
            "opened_count": session.get('opened_count', 0),
            "remaining_count": 10 - len(user_state['opened_gifts'])
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})