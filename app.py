from flask import Flask, url_for, request, redirect
import datetime

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def main_page():
    current_year = datetime.datetime.now().year
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
        }}
        nav {{
            margin: 20px 0;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        nav ul {{
            list-style-type: none;
            padding: 0;
        }}
        nav li {{
            margin: 10px 0;
        }}
        nav a {{
            text-decoration: none;
            color: #2c3e50;
            font-weight: bold;
        }}
        nav a:hover {{
            color: #e74c3c;
        }}
        footer {{
            margin-top: 30px;
            padding: 15px;
            background-color: #34495e;
            color: white;
            text-align: center;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
    </header>
    
    <nav>
        <ul>
            <li><a href="/lab1">Первая лабораторная</a></li>
        </ul>
    </nav>
    
    <footer>
        <p>Шкуропатов Андрей Александрович, ФБИ-32, 3 курс, {current_year} год</p>
    </footer>
</body>
</html>
'''

@app.route("/lab1")
@app.route("/lab1/")  
def lab1_index():
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная 1</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .content {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .menu {
            margin: 20px 0;
        }
        .menu a {
            display: inline-block;
            margin: 5px 10px 5px 0;
            padding: 10px 15px;
            background-color: #2c3e50;
            color: white;
            text-decoration: none;
            border-radius: 3px;
        }
        .menu a:hover {
            background-color: #34495e;
        }
        .back-link {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Лабораторная работа 1</h1>
    
    <div class="content">
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
        использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится 
        к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
        сознательно предоставляющих лишь самые базовые возможности.</p>
    </div>
    
    <div class="menu">
        <h3>Страницы лабораторной:</h3>
        <a href="/lab1/web">Web-сервер</a>
        <a href="/lab1/author">Автор</a>
        <a href="/lab1/image">Изображение</a>
        <a href="/lab1/counter">Счетчик</a>
        <a href="/lab1/info">Информация</a>
        <a href="/http-codes">HTTP Коды ответов</a>
        <a href="/test-errors">Тест ошибок 500</a>
        <a href="/несуществующая-страница">Тест 404 ошибки</a>
    </div>
    
    <div class="back-link">
        <a href="/">На главную</a>
    </div>
</body>
</html>
'''

@app.route("/lab1/web")
def start():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
                <a href="/lab1/author">author</a><br>
                <a href="/lab1">В меню лабы 1</a><br>
                <a href="/">На главную</a>
           </body>
        </html>""", 200, {
            'X-Server':'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Шкуропатов Андрей Александрович"
    group = "ФБИ-32"
    faculty = "ФБ"
    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a><br>
                <a href="/lab1">В меню лабы 1</a><br>
                <a href="/">На главную</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <title>Дуб</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Величественный дуб</h1>
        <img src="''' + path + '''" alt="Дуб">
        <br>
        <a href="/lab1/web">Вернуться на web</a><br>
        <a href="/lab1">В меню лабы 1</a><br>
        <a href="/">На главную</a>
    </body>
</html>
'''

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счетчик посещений</h1>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="/lab1/reset_counter">Очистить счетчик</a> | 
        <a href="/lab1/web">На web</a> | 
        <a href="/lab1">В меню лабы 1</a> | 
        <a href="/">На главную</a>
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>404 - Страница не найдена</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }
        .container {
            max-width: 600px;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
            color: #ff6b6b;
        }
        .error-title {
            font-size: 36px;
            margin: 20px 0;
            color: #ffe66d;
        }
        .error-message {
            font-size: 18px;
            line-height: 1.6;
            margin: 20px 0;
            opacity: 0.9;
        }
        .tea-cup {
            font-size: 80px;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }
        .navigation {
            margin-top: 30px;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px;
            background: #4ecdc4;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .btn:hover {
            background: transparent;
            border-color: #4ecdc4;
            transform: translateY(-2px);
        }
        .search-box {
            margin: 20px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 10px;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        .suggestions {
            margin-top: 20px;
            font-size: 14px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="tea-cup">☕</div>
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Ой! Кажется, мы потерялись в цифровом пространстве</h2>
        
        <div class="error-message">
            <p>Страница, которую вы ищете, упорхнула в параллельную вселенную или просто решила взять выходной.</p>
            <p>Возможно, она прячется за одним из этих вариантов:</p>
        </div>

        <div class="search-box">
            <p>🔍 <em>Пока вы здесь, почему бы не выпить чашечку чая?</em></p>
        </div>

        <div class="navigation">
            <a href="/" class="btn">🏠 На главную</a>
            <a href="/lab1" class="btn">📚 К лабораторным</a>
            <a href="javascript:history.back()" class="btn">↩️ Назад</a>
        </div>

        <div class="suggestions">
            <p>P.S. Если вы уверены, что страница должна быть здесь, возможно, она просто замаскировалась под ошибку 418</p>
        </div>
    </div>
</body>
</html>
''', 404

@app.route("/401")
def unauthorized():
    return '''
<!doctype html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 401

@app.route("/402")
def payment_required():
    return '''
<!doctype html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Зарезервировано для будущего использования. Изначально предназначалось для использования в системах цифровых платежей.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 402

@app.route("/403")
def forbidden():
    return '''
<!doctype html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к запрашиваемому ресурсу запрещен.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 403

@app.route("/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Указанный метод HTTP не поддерживается для данного ресурса.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 405

@app.route("/418")
def teapot():
    return '''
<!doctype html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>Я - чайник! Этот код был введен как первоапрельская шутка в 1998 году.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 418


@app.route("/http-codes")
def http_codes_menu():
    return '''
<!doctype html>
<html>
<head>
    <title>HTTP Коды ответов</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .code { margin: 10px 0; padding: 10px; border-left: 4px solid #ccc; }
        .400 { border-color: #e74c3c; }
        .401 { border-color: #e67e22; }
        .402 { border-color: #f1c40f; }
        .403 { border-color: #d35400; }
        .405 { border-color: #c0392b; }
        .418 { border-color: #8e44ad; }
    </style>
</head>
<body>
    <h1>HTTP Коды ответов</h1>
    
    <div class="code 400">
        <a href="/400">400 Bad Request</a> - Ошибка запроса
    </div>
    
    <div class="code 401">
        <a href="/401">401 Unauthorized</a> - Неавторизован
    </div>
    
    <div class="code 402">
        <a href="/402">402 Payment Required</a> - Необходима оплата
    </div>
    
    <div class="code 403">
        <a href="/403">403 Forbidden</a> - Запрещено
    </div>
    
    <div class="code 405">
        <a href="/405">405 Method Not Allowed</a> - Метод не разрешен
    </div>
    
    <div class="code 418">
        <a href="/418">418 I'm a teapot</a> - Я чайник
    </div>
    
    <br>
    <a href="/">На главную</a>
</body>
</html>
'''
@app.route("/cause-error")
def cause_error():
    """Специальный роут для вызова ошибки сервера"""
    
    error_type = request.args.get('type', 'division')
    
    if error_type == 'division':
        
        result = 10 / 0
    elif error_type == 'concat':
        
        result = 10 + "строка"
    elif error_type == 'index':
        
        arr = [1, 2, 3]
        result = arr[10]
    elif error_type == 'attribute':
        
        result = None.some_method()
    elif error_type == 'import':
        
        import non_existent_module
    else:
        
        raise Exception("Произвольная ошибка сервера!")
    
    return "Эта строка никогда не будет показана"

@app.errorhandler(500)
def internal_server_error(err):
    """Обработчик ошибки 500"""
    return '''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>500 - Ошибка сервера</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
        }
        .container {
            max-width: 700px;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }
        .error-code {
            font-size: 120px;
            font-weight: bold;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
            color: #ffe66d;
        }
        .error-title {
            font-size: 36px;
            margin: 20px 0;
            color: #ffe66d;
        }
        .error-message {
            font-size: 18px;
            line-height: 1.6;
            margin: 20px 0;
            opacity: 0.9;
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
        }
        .warning-icon {
            font-size: 80px;
            margin: 20px 0;
            animation: pulse 2s infinite;
        }
        .navigation {
            margin-top: 30px;
        }
        .btn {
            display: inline-block;
            padding: 12px 30px;
            margin: 10px;
            background: #4ecdc4;
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: bold;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }
        .btn:hover {
            background: transparent;
            border-color: #4ecdc4;
            transform: translateY(-2px);
        }
        .error-types {
            margin: 20px 0;
            text-align: left;
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
        }
        .error-types h3 {
            margin-top: 0;
            color: #ffe66d;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .tech-info {
            font-size: 14px;
            opacity: 0.7;
            margin-top: 20px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="warning-icon">⚠️</div>
        <h1 class="error-code">500</h1>
        <h2 class="error-title">Внутренняя ошибка сервера</h2>
        
        <div class="error-message">
            <p>На сервере произошла непредвиденная ошибка. Наши инженеры уже бегут с кофе и паяльниками устранять проблему!</p>
            <p>Попробуйте обновить страницу через несколько минут или вернуться на главную.</p>
        </div>

        <div class="error-types">
            <h3>Возможные причины:</h3>
            <ul>
                <li>Ошибка в программном коде</li>
                <li>Проблемы с подключением к базе данных</li>
                <li>Недостаточно памяти на сервере</li>
                <li>Временные технические неполадки</li>
            </ul>
        </div>

        <div class="navigation">
            <a href="/" class="btn">🏠 На главную</a>
            <a href="javascript:location.reload()" class="btn">🔄 Обновить</a>
            <a href="/lab1" class="btn">📚 К лабораторным</a>
        </div>

        <div class="tech-info">
            <p>Если ошибка повторяется, пожалуйста, сообщите администратору сайта.</p>
        </div>
    </div>
</body>
</html>
''', 500


@app.route("/test-errors")
def test_errors():
    """Страница для тестирования различных ошибок"""
    return '''
<!doctype html>
<html>
<head>
    <title>Тестирование ошибок</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .error-test { margin: 10px 0; padding: 10px; background: #f0f0f0; }
        .warning { color: #e74c3c; font-weight: bold; }
    </style>
</head>
<body>
    <h1>Тестирование ошибок сервера</h1>
    
    <div class="warning">
        ⚠️ Для тестирования ошибки 500 запустите сервер без флага --debug!
    </div>
    
    <div class="error-test">
        <h3>Вызвать ошибку 500:</h3>
        <a href="/cause-error?type=division">Деление на ноль</a><br>
        <a href="/cause-error?type=concat">Конкатенация числа и строки</a><br>
        <a href="/cause-error?type=index">Ошибка индекса</a><br>
        <a href="/cause-error?type=attribute">Ошибка атрибута</a><br>
        <a href="/cause-error?type=import">Ошибка импорта</a><br>
        <a href="/cause-error?type=general">Общая ошибка</a>
    </div>
    
    <br>
    <a href="/">На главную</a>
</body>
</html>
'''
if __name__ == '__main__':
    app.run(debug=False)