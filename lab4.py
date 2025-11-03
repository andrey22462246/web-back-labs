from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4',__name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error = 'Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error = 'На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 0
    x2 = int(x2) if x2 != '' else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 != '' else 1
    x2 = int(x2) if x2 != '' else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ноль в нулевой степени не определен!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, 
                              max_trees=10, min_trees=0)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Евгений Козлов', 'gender': 'male'},
    {'login': 'zxc', 'password': '666', 'name': 'Олег Бочаров', 'gender': 'male'},
    {'login': 'qwerty', 'password': 'qwerty', 'name': 'Мария Иванова', 'gender': 'female'},
    {'login': 'lol', 'password': 'kek', 'name': 'Администратор', 'gender': 'male'},
]
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("lab4/login.html", authorized=False)
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, login=login, authorized=False)
    
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, login=login, authorized=False)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            session['gender'] = user['gender']
            return render_template('lab4/login.html', name=user['name'], authorized=True)
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login=login, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    session.pop('gender', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge-form.html')
    
    temperature_str = request.form.get('temperature')
    
    if not temperature_str:
        return render_template('lab4/fridge-form.html', 
                             error='Ошибка: не задана температура')
    
    try:
        temperature = int(temperature_str)
    except ValueError:
        return render_template('lab4/fridge-form.html', 
                             error='Ошибка: введите целое число')

    if temperature < -12:
        return render_template('lab4/fridge-form.html', 
                             error='Не удалось установить температуру — слишком низкое значение',
                             temp=temperature)
    elif temperature > -1:
        return render_template('lab4/fridge-form.html', 
                             error='Не удалось установить температуру — слишком высокое значение',
                             temp=temperature)
    
    if -12 <= temperature <= -9:
        snowflakes = 3
    elif -8 <= temperature <= -5:
        snowflakes = 2
    elif -4 <= temperature <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge-form.html', 
                         success=f'Установлена температура: {temperature}°С',
                         snowflakes=snowflakes,
                         temp=temperature)

@lab4.route('/lab4/fridge')
def fridge_form():
    return render_template('lab4/fridge-form.html')

@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain-order.html')
    
    grain_type = request.form.get('grain_type')
    weight_str = request.form.get('weight')
    
    prices = {
        'barley': 12000,
        'oats': 8500,
        'wheat': 9000,
        'rye': 15000
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not weight_str:
        return render_template('lab4/grain-order.html', 
                             error='Ошибка: не указан вес',
                             grain_type=grain_type)
    
    try:
        weight = float(weight_str)
    except ValueError:
        return render_template('lab4/grain-order.html', 
                             error='Ошибка: введите корректное число для веса',
                             grain_type=grain_type)
    
    if weight <= 0:
        return render_template('lab4/grain-order.html', 
                             error='Ошибка: вес должен быть больше 0',
                             grain_type=grain_type)
    
    if weight > 100:
        return render_template('lab4/grain-order.html', 
                             error='Ошибка: такого объёма сейчас нет в наличии',
                             grain_type=grain_type,
                             weight=weight)
    
    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    
    discount_applied = False
    discount_amount = 0
    
    if weight > 10:
        discount_amount = total * 0.1
        total -= discount_amount
        discount_applied = True
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain-order.html', 
                         success=f'Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight} т. Сумма к оплате: {total:.0f} руб',
                         discount_applied=discount_applied,
                         discount_amount=discount_amount,
                         grain_type=grain_type,
                         weight=weight)

@lab4.route('/lab4/grain-order')
def grain_order_form():
    return render_template('lab4/grain-order.html')