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