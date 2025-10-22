from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
import math

lab2 = Blueprint('lab2',__name__)
flowers_list = [
    {'id': 0, 'name': 'роза', 'price': 150, 'color': '#ff6b6b'},
    {'id': 1, 'name': 'тюльпан', 'price': 80, 'color': '#e83e8c'},
    {'id': 2, 'name': 'незабудка', 'price': 60, 'color': '#4ecdc4'},
    {'id': 3, 'name': 'ромашка', 'price': 50, 'color': '#ffe66d'}
]

@lab2.route('/lab2/delete_flower/<int:flower_id>')
def lab2_delete_flower(flower_id):
    """Удаление цветка по ID"""
    try:
        # Проверяем существование цветка
        if flower_id < 0 or flower_id >= len(flowers_list):
            abort(404, description=f"Цветок с ID {flower_id} не найден")
        
        # Удаляем цветок
        deleted_flower = flowers_list.pop(flower_id)
        
        # Обновляем ID оставшихся цветов
        for i, flower in enumerate(flowers_list):
            flower['id'] = i
            
        # Перенаправляем на страницу всех цветов
        return redirect('/lab2/all_flowers')
        
    except Exception as e:
        return f'''
        <h1>Ошибка при удалении цветка</h1>
        <p>Ошибка: {str(e)}</p>
        <a href="/lab2/all_flowers">Вернуться к списку цветов</a>
        ''', 500

@lab2.route('/lab2/a')
def lab2_a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def lab2_a2():
    return 'со слешом'

@lab2.route('/lab2/flowers/<int:flower_id>')
def lab2_flowers(flower_id):
    if flower_id >= len(flowers_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
<head>
    <title>Цветок #{flower_id}</title>
    <link rel="icon" type="image/x-icon" href="/static/lab2/favicon.ico">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        .flower-info {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #e83e8c;
        }}
        .navigation {{
            margin: 20px 0;
        }}
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
        .btn:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <h1>🌺 Информация о цветке</h1>
    
    <div class="flower-info">
        <h2>Цветок #{flower_id}</h2>
        <p><strong>Название:</strong> {flowers_list[flower_id]['name']}</p>
        <p><strong>Цена:</strong> {flowers_list[flower_id]['price']} руб.</p>
        <p><strong>ID:</strong> {flower_id}</p>
        <p><strong>Всего цветов в коллекции:</strong> {len(flowers_list)}</p>
    </div>

    <div class="navigation">
        <a href="/lab2/all_flowers" class="btn">📚 Посмотреть все цветы</a>
        <a href="/lab2" class="btn">🔙 К лабораторной 2</a>
        <a href="/" class="btn">🏠 На главную</a>
    </div>
</body>
</html>
'''

@lab2.route('/lab2/add_flower')
def lab2_add_flower():
    """Добавление нового цветка через форму"""
    name = request.args.get('name')
    price = request.args.get('price')
    color = request.args.get('color', '#ff6b6b')
    
    if name and price:
        try:
            new_flower = {
                'id': len(flowers_list),
                'name': name,
                'price': int(price),
                'color': color
            }
            flowers_list.append(new_flower)
            return render_template('lab2/add_flower.html', name=name)
        except ValueError:
            return "Ошибка: цена должна быть числом", 400
    
    return render_template('lab2/add_flower.html')

@lab2.route('/lab2/all_flowers')
def lab2_all_flowers():
    """Роут для вывода всех цветов и их количества"""
    return render_template('lab2/all_flowers.html', flowers_list=flowers_list)

@lab2.route('/lab2/clear_flowers')
def lab2_clear_flowers():
    """Роут для очистки списка цветов"""
    flowers_list.clear()
    return '''
<!doctype html>
<html>
<head>
    <title>Коллекция очищена</title>
    <link rel="icon" type="image/x-icon" href="/static/lab2/favicon.ico">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        .success-message {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 30px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #17a2b8;
            text-align: center;
        }
        .navigation {
            margin: 30px 0;
            text-align: center;
        }
        .btn {
            display: inline-block;
            padding: 12px 25px;
            margin: 8px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        .btn-success {
            background-color: #28a745;
        }
        .btn-success:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <h1>🗑️ Коллекция цветов очищена</h1>
    
    <div class="success-message">
        <h2>✅ Все цветы успешно удалены!</h2>
        <p>Коллекция цветов была полностью очищена.</p>
        <p style="font-size: 48px; margin: 20px 0;">🌱</p>
        <p>Теперь вы можете начать новую коллекцию!</p>
    </div>

    <div class="navigation">
        <a href="/lab2/all_flowers" class="btn">📚 Перейти к коллекции</a>
        <a href="/lab2" class="btn">🔙 К лабораторной 2</a>
        <a href="/" class="btn">🏠 На главную</a>
    </div>
</body>
</html>
'''

@lab2.route('/lab2/example')
def lab2_example():
    name = 'Шкуропатов Андрей'
    number_lab = 2
    number_course = 3
    number_group = 32
    fruits = [
        {'name':'Яблоки', 'price': 100},
        {'name':'Груши', 'price': 120},
        {'name':'Апельсины', 'price': 80},
        {'name':'Мандарины', 'price': 95},
        {'name':'Манго', 'price': 321}
    ]
    return render_template('lab2/example.html', 
                         name=name, 
                         number_lab=number_lab, 
                         number_course=number_course, 
                         number_group=number_group, 
                         fruits=fruits)

@lab2.route('/lab2/')
def lab2_index():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/filters')
def lab2_filters():
    """Страница с демонстрацией фильтров"""
    phrase = "О сколько нам открытий чудных готовит просвещенья дух"
    return render_template('lab2/filters.html', phrase=phrase)

# Калькулятор
@lab2.route('/lab2/calc/')
def lab2_calc_default():
    """Перенаправление на калькулятор с значениями по умолчанию"""
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def lab2_calc_single(a):
    """Перенаправление на калькулятор с одним числом и вторым по умолчанию"""
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def lab2_calc(a, b):
    """Калькулятор с двумя числами"""
    
    # Выполняем математические операции
    operations = {
        'Сложение': f'{a} + {b} = {a + b}',
        'Вычитание': f'{a} - {b} = {a - b}',
        'Умножение': f'{a} × {b} = {a * b}',
        'Деление': f'{a} ÷ {b} = {a / b:.2f}' if b != 0 else f'{a} ÷ {b} = Ошибка (деление на ноль)',
        'Возведение в степень': f'{a}<sup>{b}</sup> = {a ** b}',
        'Целочисленное деление': f'{a} // {b} = {a // b}' if b != 0 else f'{a} // {b} = Ошибка (деление на ноль)',
        'Остаток от деления': f'{a} % {b} = {a % b}' if b != 0 else f'{a} % {b} = Ошибка (деление на ноль)',
    }
    
    # Дополнительные математические функции
    additional_ops = {
        'Квадратный корень a': f'√{a} = {math.sqrt(a):.2f}' if a >= 0 else f'√{a} = Ошибка (отрицательное число)',
        'Квадратный корень b': f'√{b} = {math.sqrt(b):.2f}' if b >= 0 else f'√{b} = Ошибка (отрицательное число)',
        'Модуль a': f'|{a}| = {abs(a)}',
        'Модуль b': f'|{b}| = {abs(b)}',
        'Факториал a': f'{a}! = {math.factorial(a)}' if a >= 0 and a <= 20 else f'{a}! = Слишком большое число',
        'Факториал b': f'{b}! = {math.factorial(b)}' if b >= 0 and b <= 20 else f'{b}! = Слишком большое число',
    }
    
    return render_template('lab2/calc.html', 
                         a=a, 
                         b=b, 
                         operations=operations, 
                         additional_ops=additional_ops)

books_list = [
    {'author': 'Фёдор Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Лев Толстой', 'title': 'Война и мир', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'author': 'Михаил Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Антон Чехов', 'title': 'Рассказы', 'genre': 'Рассказ', 'pages': 320},
    {'author': 'Александр Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 240},
    {'author': 'Николай Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Иван Тургенев', 'title': 'Отцы и дети', 'genre': 'Роман', 'pages': 288},
    {'author': 'Александр Островский', 'title': 'Гроза', 'genre': 'Драма', 'pages': 120},
    {'author': 'Михаил Лермонтов', 'title': 'Герой нашего времени', 'genre': 'Роман', 'pages': 224},
    {'author': 'Иван Гончаров', 'title': 'Обломов', 'genre': 'Роман', 'pages': 640},
    {'author': 'Александр Грибоедов', 'title': 'Горе от ума', 'genre': 'Комедия', 'pages': 160},
    {'author': 'Николай Лесков', 'title': 'Левша', 'genre': 'Повесть', 'pages': 96}
]

@lab2.route('/lab2/books')
def lab2_books():
    """Страница со списком книг"""
    return render_template('lab2/books.html', books=books_list)
    
# Список автомобилей
cars_list = [
    {
        'name': 'Tesla Model S',
        'image': 'lab2/tesla_model_s.jpg',
        'description': 'Электрический седан премиум-класса с автопилотом и ускорением 0-100 км/ч за 2.1 секунды'
    },
    {
        'name': 'BMW M5',
        'image': 'lab2/bmw_m5.jpg', 
        'description': 'Спортивный седан с двигателем V8 мощностью 600 л.с. и полным приводом xDrive'
    },
    {
        'name': 'Mercedes-Benz S-Class',
        'image': 'lab2/mercedes_s_class.jpg',
        'description': 'Флагманский седан люкс-класса с технологиями автономного вождения и роскошным салоном'
    },
    {
        'name': 'Audi RS6',
        'image': 'lab2/audi_rs6.jpg',
        'description': 'Универсал с двигателем V8 би-турбо мощностью 600 л.с. и спортивной подвеской'
    },
    {
        'name': 'Porsche 911',
        'image': 'lab2/porsche_911.jpg',
        'description': 'Легендарный спортивный автомобиль с задним расположением двигателя и уникальным дизайном'
    },
    {
        'name': 'Lamborghini Huracan',
        'image': 'lab2/lamborghini_huracan.jpg',
        'description': 'Суперкар с двигателем V10 мощностью 640 л.с. и агрессивным дизайном'
    },
    {
        'name': 'Ferrari F8 Tributo',
        'image': 'lab2/ferrari_f8.jpg',
        'description': 'Среднемоторный спорткар с двигателем V8 мощностью 720 л.с. и технологиями F1'
    },
    {
        'name': 'Rolls-Royce Phantom',
        'image': 'lab2/rolls_royce_phantom.jpg',
        'description': 'Ультра-люксовый седан ручной сборки с бесшумным салоном и индивидуальным интерьером'
    },
    {
        'name': 'Bentley Continental GT',
        'image': 'lab2/bentley_continental.jpg',
        'description': 'Гранд-турер с двигателем W12 и сочетанием роскоши с высокими динамическими характеристиками'
    },
    {
        'name': 'Ford Mustang',
        'image': 'lab2/ford_mustang.jpg',
        'description': 'Американский маслкар с двигателем V8 и культовым дизайном'
    },
    {
        'name': 'Chevrolet Corvette',
        'image': 'lab2/chevrolet_corvette.jpg',
        'description': 'Спортивный автомобиль с переднем расположением двигателя V8 и доступной ценой'
    },
    {
        'name': 'Jeep Wrangler',
        'image': 'lab2/jeep_wrangler.jpg',
        'description': 'Внедорожник с подключаемым полным приводом и съемными дверями для офф-роуда'
    },
    {
        'name': 'Land Rover Defender',
        'image': 'lab2/land_rover_defender.jpg',
        'description': 'Легендарный внедорожник с современными технологиями и выдающейся проходимостью'
    },
    {
        'name': 'Toyota Land Cruiser',
        'image': 'lab2/toyota_land_cruiser.jpg',
        'description': 'Надежный внедорожник с рамной конструкцией и репутацией неубиваемого автомобиля'
    },
    {
        'name': 'Volkswagen Golf GTI',
        'image': 'lab2/vw_golf_gti.jpg',
        'description': 'Хот-хэтч с богатой спортивной историей и отличной управляемостью'
    },
    {
        'name': 'Subaru WRX STI',
        'image': 'lab2/subaru_wrx.jpg',
        'description': 'Спортивный седан с оппозитным двигателем и симметричным полным приводом'
    },
    {
        'name': 'Nissan GT-R',
        'image': 'lab2/nissan_gtr.jpg',
        'description': 'Японский суперкар с двигателем V6 би-турбо и прозвищем "Бог"'
    },
    {
        'name': 'Mazda MX-5 Miata',
        'image': 'lab2/mazda_mx5.jpg',
        'description': 'Компактный родстер с идеальной развесовкой и доступной ценой для настоящего драйва'
    },
    {
        'name': 'Honda Civic Type R',
        'image': 'lab2/honda_civic_type_r.jpg',
        'description': 'Хот-хэтч с турбодвигателем и рекордом на Нюрбургринге среди переднеприводных автомобилей'
    },
    {
        'name': 'McLaren 720S',
        'image': 'lab2/mclaren_720s.jpg',
        'description': 'Суперкар с карбоновым монококом и двигателем V8 мощностью 720 л.с.'
    },
    {
        'name': 'Aston Martin DB11',
        'image': 'lab2/aston_martin_db11.jpg',
        'description': 'Гранд-турер с элегантным британским дизайном и двигателем от Mercedes-AMG'
    },
    {
        'name': 'Lexus LC 500',
        'image': 'lab2/lexus_lc500.jpg',
        'description': 'Купэ люкс-класса с атмосферным двигателем V8 и футуристичным дизайном'
    }
]

@lab2.route('/lab2/cars')
def lab2_cars():
    """Страница со списком автомобилей"""
    return render_template('lab2/cars.html', cars=cars_list)