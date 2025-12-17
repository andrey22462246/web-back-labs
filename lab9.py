import json
import random
import hashlib
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
        "text": "🎅 ОСОБЫЙ ПОДАРОК: Пусть новый год станет годом великих открытий и успехов!",
        "gift_name": "Волшебная карта мира",
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

game_states = {}

def get_user_key():
    if session.get('authenticated'):
        username = session.get('username', '')
        session_id = session.get('session_id', '')
        return f"{username}_{session_id}"
    return session.get('session_id', 'default')

def generate_gift_positions():
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

def init_game_state():
    user_key = get_user_key()
    if user_key not in game_states:
        game_states[user_key] = {
            'gift_positions': generate_gift_positions(),
            'opened_gifts': [],
            'opened_count': 0
        }
    return game_states[user_key]

@lab9.route('/lab9')
def lab9_route():
    if 'session_id' not in session:
        session_id = f"{random.randint(10000, 99999)}_{random.randint(10000, 99999)}_{random.randint(10000, 99999)}"
        session['session_id'] = session_id
    
    game_state = init_game_state()
    
    opened_gifts = game_state['opened_gifts']
    opened_count = game_state['opened_count']
    is_authenticated = session.get('authenticated', False)
    username = session.get('username', '')
    
    positions = game_state['gift_positions']
    for pos in positions:
        pos['opened'] = pos['id'] in opened_gifts
    
    available = 10 if is_authenticated else 9
    
    return render_template('lab9/lab9.html',
                         opened_count=opened_count,
                         remaining_count=10 - len(opened_gifts),
                         available_count=available,
                         authenticated=is_authenticated,
                         username=username)

@lab9.route('/lab9/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"success": False, "error": "Введите имя пользователя и пароль"})
        
        if username in USERS and USERS[username] == password:
            old_key = get_user_key()
            
            session['authenticated'] = True
            session['username'] = username
            
            if old_key != get_user_key():
                init_game_state()
            
            return jsonify({
                "success": True,
                "message": f"Добро пожаловать, {username}! 🎅",
                "username": username
            })
        else:
            return jsonify({"success": False, "error": "Неверное имя пользователя или пароль"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/logout', methods=['POST'])
def logout():
    old_key = get_user_key()
    session.pop('authenticated', None)
    session.pop('username', None)
    
    if old_key != get_user_key():
        init_game_state()
    
    return jsonify({
        "success": True,
        "message": "Вы вышли из системы"
    })

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    try:
        data = request.get_json()
        gift_id = data.get('gift_id')
        
        if gift_id is None or not isinstance(gift_id, int) or gift_id < 0 or gift_id >= 10:
            return jsonify({"success": False, "error": "Неверный ID подарка"})
        
        game_state = init_game_state()
        opened_gifts = game_state['opened_gifts']
        
        if gift_id in opened_gifts:
            return jsonify({"success": False, "error": "Этот подарок уже открыт"})
        
        opened_count = game_state['opened_count']
        if opened_count >= 3:
            return jsonify({"success": False, "error": "Вы уже открыли 3 подарка"})
        
        congrat = CONGRATULATIONS[gift_id]
        if congrat["requires_auth"] and not session.get('authenticated'):
            return jsonify({
                "success": False,
                "error": "Этот подарок доступен только для авторизованных пользователей",
                "requires_auth": True
            })
        
        opened_gifts.append(gift_id)
        game_state['opened_gifts'] = opened_gifts
        game_state['opened_count'] = opened_count + 1
        
        positions = game_state['gift_positions']
        for pos in positions:
            if pos['id'] == gift_id:
                pos['opened'] = True
                break
        
        user_key = get_user_key()
        game_states[user_key] = game_state
        
        return jsonify({
            "success": True,
            "congratulation": congrat,
            "opened_count": game_state['opened_count'],
            "remaining_count": 10 - len(opened_gifts)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Ошибка: {str(e)}"})

@lab9.route('/lab9/santa_refill', methods=['POST'])
def santa_refill():
    try:
        if not session.get('authenticated', False):
            return jsonify({"success": False, "error": "Требуется авторизация"})
        
        user_key = get_user_key()
        game_states[user_key] = {
            'gift_positions': generate_gift_positions(),
            'opened_gifts': [],
            'opened_count': 0
        }
        
        return jsonify({
            "success": True,
            "message": "🎅 Дед Мороз обновил подарки!",
            "opened_count": 0,
            "remaining_count": 10
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@lab9.route('/lab9/get_state', methods=['GET'])
def get_state():
    try:
        game_state = init_game_state()
        positions = game_state['gift_positions']
        opened_gifts = game_state['opened_gifts']
        is_authenticated = session.get('authenticated', False)
        
        for pos in positions:
            pos['opened'] = pos['id'] in opened_gifts
        
        available_count = 10
        if not is_authenticated:
            locked_count = sum(1 for pos in positions if pos.get('requires_auth') and not pos['opened'])
            available_count = 10 - locked_count
        
        return jsonify({
            "success": True,
            "positions": positions,
            "opened_gifts": opened_gifts,
            "opened_count": game_state['opened_count'],
            "remaining_count": 10 - len(opened_gifts),
            "available_count": available_count,
            "authenticated": is_authenticated,
            "username": session.get('username', '')
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})