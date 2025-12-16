import json
import random
from flask import Blueprint, render_template, request, jsonify, session

lab9 = Blueprint('lab9', __name__, template_folder='templates')

CONGRATULATIONS = [
    {
        "id": 0,
        "text": "Пусть Новый год принесёт много радости, счастья и удачи! Желаем исполнения всех желаний и ярких впечатлений!",
        "gift_name": "Золотой колокольчик",
        "image": "gift1.png",
        "requires_auth": False
    },
    {
        "id": 1,
        "text": "С Новым годом! Пусть ангел-хранитель оберегает вас, а Дед Мороз исполнит самые заветные мечты!",
        "gift_name": "Волшебный шар",
        "image": "gift2.png",
        "requires_auth": False
    },
    {
        "id": 2,
        "text": "Желаем, чтобы новый год был наполнен уютом, теплом семейного очага и приятными сюрпризами!",
        "gift_name": "Тёплый плед",
        "image": "gift3.png",
        "requires_auth": False
    },
    {
        "id": 3,
        "text": "Пусть каждый день нового года будет похож на сказку, полную чудес, волшебства и добрых встреч!",
        "gift_name": "Книга сказок",
        "image": "gift4.png",
        "requires_auth": False
    },
    {
        "id": 4,
        "text": "С новым годом! Желаем крепкого здоровья, финансового благополучия и карьерного роста!",
        "gift_name": "Золотой ключ",
        "image": "gift5.png",
        "requires_auth": False
    },
    {
        "id": 5,
        "text": "Пусть новый год подарит море улыбок, верных друзей и незабываемых путешествий!",
        "gift_name": "Чемодан мечты",
        "image": "gift6.png",
        "requires_auth": False
    },
    {
        "id": 6,
        "text": "Желаем, чтобы снегопад удачи сыпался на вас весь год, а каждый день приносил новые победы!",
        "gift_name": "Снежный глобус",
        "image": "gift7.png",
        "requires_auth": False
    },
    {
        "id": 7,
        "text": "С Новым годом! Пусть ваша ёлка будет самой красивой, а праздник — самым весёлым!",
        "gift_name": "Ёлочная игрушка",
        "image": "gift8.png",
        "requires_auth": False
    },
    {
        "id": 8,
        "text": "Желаем найти свою золотую жилу в новом году! Пусть удача всегда будет на вашей стороне!",
        "gift_name": "Сундук с сокровищами",
        "image": "gift9.png",
        "requires_auth": False
    },
    {
        "id": 9,
        "text": " Пусть новый год станет годом великих открытий и успехов!",
        "gift_name": "Волшебный карта",
        "image": "gift10.png",
        "requires_auth": True  
    }
]


USERS = {
    "user": "123",  
    "admin": "admin",
    "santa": "2025",
    "гость": "праздник"
}


gift_states = {}

def generate_gift_positions():
    """Генерация СЛУЧАЙНЫХ позиций для подарков без наложения"""
    positions = []
    occupied_positions = []  
    
    
    all_gift_ids = list(range(10))
    random.shuffle(all_gift_ids) 
    
    for gift_id in all_gift_ids:
        placed = False
        attempts = 0
        
        while not placed and attempts < 100:  
            attempts += 1
            
            
            top = random.randint(5, 75)  
            left = random.randint(5, 85)  
            
            
            
            overlaps = False
            for occupied in occupied_positions:
                
                if (abs(top - occupied['top']) < 15 and 
                    abs(left - occupied['left']) < 15):
                    overlaps = True
                    break
            
            if not overlaps:
                positions.append({
                    "id": gift_id,
                    "top": f"{top}%",
                    "left": f"{left}%",
                    "opened": False,
                    "requires_auth": CONGRATULATIONS[gift_id]["requires_auth"]
                })
                occupied_positions.append({"top": top, "left": left})
                placed = True
        
        
        if not placed:
            top = random.randint(5, 75)
            left = random.randint(5, 85)
            positions.append({
                "id": gift_id,
                "top": f"{top}%",
                "left": f"{left}%",
                "opened": False,
                "requires_auth": CONGRATULATIONS[gift_id]["requires_auth"]
            })
    
    return positions

@lab9.route('/lab9')
def lab9_route():
    """Главная страница"""
    if 'user_id' not in session:
        session['user_id'] = f"user_{random.randint(1000, 9999)}"
        session['opened_count'] = 0
    
    user_id = session['user_id']
    
    if user_id not in gift_states:
        
        gift_states[user_id] = {
            "positions": generate_gift_positions(),
            "opened_gifts": [],
            "congratulations": CONGRATULATIONS
        }
    
    is_authenticated = session.get('authenticated', False)
    opened_count = session.get('opened_count', 0)
    total_opened = len(gift_states[user_id]['opened_gifts'])
    remaining = 10 - total_opened
    
    
    available = 10 if is_authenticated else 9
    
    return render_template('lab9/lab9.html',
                         opened_count=opened_count,
                         remaining_count=remaining,
                         available_count=available,
                         user_id=user_id,
                         authenticated=is_authenticated,
                         username=session.get('username', ''))

@lab9.route('/lab9/login', methods=['POST'])
def login():
    """Авторизация с проверкой пароля"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                "success": False,
                "error": "Введите имя пользователя и пароль"
            })
        
        
        if username in USERS and USERS[username] == password:
            session['authenticated'] = True
            session['username'] = username
            
            return jsonify({
                "success": True,
                "message": f"Добро пожаловать, {username}! 🎅 Теперь доступен особый подарок!",
                "username": username
            })
        else:
            return jsonify({
                "success": False,
                "error": "Неверное имя пользователя или пароль"
            })
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/logout', methods=['POST'])
def logout():
    """Выход"""
    session.pop('authenticated', None)
    session.pop('username', None)
    
    return jsonify({
        "success": True,
        "message": "Вы вышли из системы"
    })

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    """Открытие подарка"""
    try:
        data = request.get_json()
        gift_id = data.get('gift_id')
        
        if gift_id is None or not isinstance(gift_id, int) or gift_id < 0 or gift_id >= 10:
            return jsonify({"success": False, "error": "Неверный ID подарка"})
        
        user_id = session.get('user_id')
        if not user_id or user_id not in gift_states:
            return jsonify({"success": False, "error": "Сессия не найдена"})
        
        user_state = gift_states[user_id]
        
        
        if gift_id in user_state['opened_gifts']:
            return jsonify({
                "success": False, 
                "error": "Этот подарок уже открыт"
            })
        
        
        opened_count = session.get('opened_count', 0)
        if opened_count >= 3:
            return jsonify({
                "success": False,
                "error": "Вы уже открыли 3 подарка"
            })
        
        
        congrat = CONGRATULATIONS[gift_id]
        if congrat["requires_auth"] and not session.get('authenticated'):
            return jsonify({
                "success": False,
                "error": "Этот особый подарок доступен только для авторизованных пользователей",
                "requires_auth": True
            })
        
        
        user_state['opened_gifts'].append(gift_id)
        session['opened_count'] = opened_count + 1
        
        
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
        return jsonify({"success": False, "error": f"Ошибка: {str(e)}"})

@lab9.route('/lab9/santa_refill', methods=['POST'])
def santa_refill():
    """Дед Мороз обновляет подарки - только для авторизованных"""
    try:
        
        if not session.get('authenticated', False):
            return jsonify({
                "success": False,
                "error": "Эта функция доступна только для авторизованных пользователей"
            })
        
        user_id = session.get('user_id')
        if user_id in gift_states:
            
            gift_states[user_id] = {
                "positions": generate_gift_positions(),
                "opened_gifts": [],  
                "congratulations": CONGRATULATIONS
            }
        
        
        session['opened_count'] = 0
        
        return jsonify({
            "success": True,
            "message": "🎅 Дед Мороз обновил подарки! Позиции подарков изменены.",
            "opened_count": 0,
            "remaining_count": 10
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/get_state', methods=['GET'])
def get_state():
    """Получение состояния"""
    try:
        user_id = session.get('user_id')
        if not user_id or user_id not in gift_states:
            return jsonify({"success": False, "error": "Сессия не найдена"})
        
        user_state = gift_states[user_id]
        is_authenticated = session.get('authenticated', False)
        
        
        available_count = 10
        if not is_authenticated:
            
            locked_count = sum(1 for pos in user_state['positions'] 
                             if pos.get('requires_auth') and not pos['opened'])
            available_count = 10 - locked_count
        
        return jsonify({
            "success": True,
            "positions": user_state['positions'],
            "opened_gifts": user_state['opened_gifts'],
            "opened_count": session.get('opened_count', 0),
            "remaining_count": 10 - len(user_state['opened_gifts']),
            "available_count": available_count,
            "authenticated": is_authenticated,
            "username": session.get('username', '')
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})