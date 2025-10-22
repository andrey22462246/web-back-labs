from flask import Blueprint, render_template, request, make_response, redirect, url_for
lab3 = Blueprint('lab3',__name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'green')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user']='Заполните поле!'
    age = request.args.get('age')
    if user == '':
        errors['age']='Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай – 80 рублей, зелёный – 70 рублей.
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удорожает напиток на 30 рублей, а сахара – на 10.
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)
    

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', '0')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    # Получаем параметры из формы
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    
    # Если есть переданные параметры, устанавливаем куки
    if any([color, bg_color, font_size, font_family]):
        resp = make_response(redirect('/lab3/settings'))
        
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
            
        return resp
    
    # Если параметров нет, отображаем страницу с текущими значениями
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    
    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_family=font_family)

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket_form.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
    
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance') == 'on'
    
    
    errors = []
    
    if not fio:
        errors.append("ФИО пассажира обязательно")
    if not shelf:
        errors.append("Выберите тип полки")
    if not age:
        errors.append("Возраст обязателен")
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors.append("Возраст должен быть от 1 до 120 лет")
    if not departure:
        errors.append("Пункт выезда обязателен")
    if not destination:
        errors.append("Пункт назначения обязателен")
    if not date:
        errors.append("Дата поездки обязательна")
    
    if errors:
        
        return render_template('lab3/ticket_form.html', 
                             errors=errors,
                             fio=fio, shelf=shelf, bedding=bedding, luggage=luggage,
                             age=age, departure=departure, destination=destination,
                             date=date, insurance=insurance)
    
    
    age_int = int(age)
    is_child = age_int < 18
    
    base_price = 700 if is_child else 1000
    
    shelf_price = 0
    if shelf in ['lower', 'lower_side']:
        shelf_price = 100
    
    bedding_price = 75 if bedding else 0
    luggage_price = 250 if luggage else 0
    insurance_price = 150 if insurance else 0
    
    total_price = base_price + shelf_price + bedding_price + luggage_price + insurance_price
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, bedding=bedding, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, is_child=is_child,
                         base_price=base_price, shelf_price=shelf_price,
                         total_price=total_price)


products = [
    {'id': 1, 'name': 'iPhone 15 Pro', 'brand': 'Apple', 'price': 99990, 'color': 'Титановый', 'storage': '128GB'},
    {'id': 2, 'name': 'Samsung Galaxy S24', 'brand': 'Samsung', 'price': 79990, 'color': 'Черный', 'storage': '256GB'},
    {'id': 3, 'name': 'Xiaomi 14', 'brand': 'Xiaomi', 'price': 59990, 'color': 'Белый', 'storage': '256GB'},
    {'id': 4, 'name': 'Google Pixel 8', 'brand': 'Google', 'price': 54990, 'color': 'Серый', 'storage': '128GB'},
    {'id': 5, 'name': 'OnePlus 12', 'brand': 'OnePlus', 'price': 64990, 'color': 'Зеленый', 'storage': '256GB'},
    {'id': 6, 'name': 'iPhone 14', 'brand': 'Apple', 'price': 69990, 'color': 'Синий', 'storage': '128GB'},
    {'id': 7, 'name': 'Samsung Galaxy A54', 'brand': 'Samsung', 'price': 29990, 'color': 'Фиолетовый', 'storage': '128GB'},
    {'id': 8, 'name': 'Xiaomi Redmi Note 13', 'brand': 'Xiaomi', 'price': 19990, 'color': 'Черный', 'storage': '128GB'},
    {'id': 9, 'name': 'Realme 11 Pro+', 'brand': 'Realme', 'price': 24990, 'color': 'Золотой', 'storage': '256GB'},
    {'id': 10, 'name': 'Nothing Phone 2', 'brand': 'Nothing', 'price': 44990, 'color': 'Белый', 'storage': '256GB'},
    {'id': 11, 'name': 'iPhone 15 Pro Max', 'brand': 'Apple', 'price': 129990, 'color': 'Титановый', 'storage': '256GB'},
    {'id': 12, 'name': 'Samsung Galaxy Z Flip5', 'brand': 'Samsung', 'price': 89990, 'color': 'Фиолетовый', 'storage': '256GB'},
    {'id': 13, 'name': 'Google Pixel 7a', 'brand': 'Google', 'price': 34990, 'color': 'Голубой', 'storage': '128GB'},
    {'id': 14, 'name': 'Xiaomi Poco X6 Pro', 'brand': 'Xiaomi', 'price': 27990, 'color': 'Желтый', 'storage': '256GB'},
    {'id': 15, 'name': 'Samsung Galaxy S23 FE', 'brand': 'Samsung', 'price': 49990, 'color': 'Кремовый', 'storage': '128GB'},
    {'id': 16, 'name': 'iPhone SE', 'brand': 'Apple', 'price': 39990, 'color': 'Красный', 'storage': '64GB'},
    {'id': 17, 'name': 'Motorola Edge 40', 'brand': 'Motorola', 'price': 37990, 'color': 'Черный', 'storage': '256GB'},
    {'id': 18, 'name': 'Honor 90', 'brand': 'Honor', 'price': 32990, 'color': 'Изумрудный', 'storage': '256GB'},
    {'id': 19, 'name': 'Vivo V29', 'brand': 'Vivo', 'price': 41990, 'color': 'Красный', 'storage': '256GB'},
    {'id': 20, 'name': 'Oppo Reno 10', 'brand': 'Oppo', 'price': 35990, 'color': 'Синий', 'storage': '256GB'},
    {'id': 21, 'name': 'Asus ROG Phone 8', 'brand': 'Asus', 'price': 79990, 'color': 'Черный', 'storage': '256GB'},
    {'id': 22, 'name': 'Sony Xperia 5 V', 'brand': 'Sony', 'price': 74990, 'color': 'Синий', 'storage': '128GB'},
    {'id': 23, 'name': 'Nokia G42', 'brand': 'Nokia', 'price': 15990, 'color': 'Фиолетовый', 'storage': '128GB'},
    {'id': 24, 'name': 'Tecno Camon 20', 'brand': 'Tecno', 'price': 12990, 'color': 'Зеленый', 'storage': '128GB'},
    {'id': 25, 'name': 'Infinix Note 30', 'brand': 'Infinix', 'price': 14990, 'color': 'Черный', 'storage': '256GB'}
]


min_price_all = min(product['price'] for product in products)
max_price_all = max(product['price'] for product in products)

@lab3.route('/lab3/products')
def products_search():
    
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    
    min_price_form = request.args.get('min_price')
    max_price_form = request.args.get('max_price')
    reset = request.args.get('reset')
    
    
    if reset:
        resp = make_response(redirect('/lab3/products'))
        resp.set_cookie('min_price', '', expires=0)
        resp.set_cookie('max_price', '', expires=0)
        return resp
    
    
    if min_price_form is not None or max_price_form is not None:
        
        min_price = min_price_form
        max_price = max_price_form
        
        
        resp = make_response(redirect('/lab3/products'))
        if min_price_form:
            resp.set_cookie('min_price', min_price_form)
        if max_price_form:
            resp.set_cookie('max_price', max_price_form)
        return resp
    else:
        
        min_price = min_price_cookie
        max_price = max_price_cookie
    
    
    filtered_products = products.copy()
    
    if min_price:
        try:
            min_val = int(min_price)
            filtered_products = [p for p in filtered_products if p['price'] >= min_val]
        except ValueError:
            pass
    
    if max_price:
        try:
            max_val = int(max_price)
            filtered_products = [p for p in filtered_products if p['price'] <= max_val]
        except ValueError:
            pass
    
    
    if min_price and max_price:
        try:
            if int(min_price) > int(max_price):
                min_price, max_price = max_price, min_price
                
                resp = make_response(redirect('/lab3/products'))
                resp.set_cookie('min_price', min_price)
                resp.set_cookie('max_price', max_price)
                return resp
        except ValueError:
            pass
    
    return render_template('lab3/products.html',
                         products=filtered_products,
                         min_price=min_price or '',
                         max_price=max_price or '',
                         min_price_all=min_price_all,
                         max_price_all=max_price_all,
                         total_found=len(filtered_products),
                         total_all=len(products))