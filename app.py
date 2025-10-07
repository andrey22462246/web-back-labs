from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import math

app = Flask(__name__)

error_404_log = []

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
            padding: 8px 15px;
            border-radius: 5px;
            transition: all 0.3s ease;
            display: block;
        }}
        nav a:hover {{
            background-color: #2c3e50;
            color: white;
        }}
        footer {{
            margin-top: 30px;
            padding: 15px;
            background-color: #34495e;
            color: white;
            text-align: center;
            border-radius: 5px;
        }}
        .lab-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .lab-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 4px solid #007bff;
        }}
        .lab-card h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .lab-card.lab1 {{
            border-left-color: #e74c3c;
        }}
        .lab-card.lab2 {{
            border-left-color: #27ae60;
        }}
    </style>
</head>
<body>
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
    </header>
    
    <nav>
        <h3>Быстрая навигация:</h3>
        <ul>
            <li><a href="/lab1">🔧 Лабораторная работа 1</a></li>
            <li><a href="/lab2">🚀 Лабораторная работа 2</a></li>
        </ul>
    </nav>

    <div class="lab-links">
        <div class="lab-card lab1">
            <h3>📋 Лабораторная работа 1</h3>
            <p>Основы Flask: роутинг, обработка ошибок, заголовки</p>
            <a href="/lab1">Перейти к лабораторной →</a>
        </div>
        
        <div class="lab-card lab2">
            <h3>🚀 Лабораторная работа 2</h3>
            <p>Шаблоны Jinja2: наследование, фильтры, циклы</p>
            <a href="/lab2">Перейти к лабораторной →</a>
        </div>
    </div>
    
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
        .routes {
            margin: 30px 0;
            padding: 20px;
            background-color: #e9ecef;
            border-radius: 5px;
        }
        .routes h2 {
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 10px;
        }
        .route-list {
            list-style-type: none;
            padding: 0;
        }
        .route-list li {
            margin: 8px 0;
            padding: 5px;
        }
        .route-list a {
            color: #2c3e50;
            text-decoration: none;
            font-weight: bold;
        }
        .route-list a:hover {
            color: #e74c3c;
            text-decoration: underline;
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
    </div>

    <div class="routes">
        <h2>Список роутов</h2>
        <ul class="route-list">
            <li>📋 <a href="/">Главная страница</a> (/, /index)</li>
            <li>🔧 <a href="/lab1">Меню лабораторной 1</a> (/lab1)</li>
            <li>🌐 <a href="/lab1/web">Web-сервер</a> (/lab1/web)</li>
            <li>👤 <a href="/lab1/author">Информация об авторе</a> (/lab1/author)</li>
            <li>🖼️ <a href="/lab1/image">Изображение дуба</a> (/lab1/image)</li>
            <li>🔢 <a href="/lab1/counter">Счетчик посещений</a> (/lab1/counter)</li>
            <li>🔄 <a href="/lab1/reset_counter">Сброс счетчика</a> (/lab1/reset_counter)</li>
            <li>ℹ️ <a href="/lab1/info">Информация (редирект)</a> (/lab1/info)</li>
            <li>🚫 <a href="/lab1/несуществующая">Тест 404 ошибки</a></li>
            <li>⚡ <a href="/test-errors">Тест ошибок 500</a> (/test-errors)</li>
            <li>🐞 <a href="/cause-error">Вызов ошибки сервера</a> (/cause-error)</li>
            <li>📊 <a href="/http-codes">HTTP коды ответов</a> (/http-codes)</li>
            <li>❌ <a href="/400">400 Bad Request</a> (/400)</li>
            <li>🔐 <a href="/401">401 Unauthorized</a> (/401)</li>
            <li>💳 <a href="/402">402 Payment Required</a> (/402)</li>
            <li>🚷 <a href="/403">403 Forbidden</a> (/403)</li>
            <li>📡 <a href="/405">405 Method Not Allowed</a> (/405)</li>
            <li>🍵 <a href="/418">418 I'm a teapot</a> (/418)</li>
            <li>✅ <a href="/created">201 Created</a> (/created)</li>
        </ul>
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
    
    headers = {
        'Content-Language': 'ru',  
        'X-Developer': 'Shkuropatov-Andrey',  
        'X-University': 'NSTU-FB',  
        'X-Image-Description': 'Mighty oak tree in the forest',  
        'X-Lab-Number': '1'  
    }
    
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
''', 200, headers  

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
    
    client_ip = request.remote_addr
    access_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')
    
    
    log_entry = {
        'ip': client_ip,
        'date': access_date,
        'url': requested_url,
        'user_agent': user_agent
    }
    error_404_log.append(log_entry)
    
    
    if len(error_404_log) > 20:
        error_404_log.pop(0)
    
    
    log_html = ""
    for entry in reversed(error_404_log):  
        log_html += f'''
        <div class="log-entry">
            <div class="log-ip">📍 {entry['ip']}</div>
            <div class="log-date">📅 {entry['date']}</div>
            <div class="log-url">🌐 {entry['url']}</div>
            <div class="log-agent">🖥️ {entry['user_agent'][:50]}...</div>
        </div>
        '''
    
    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>404 - Страница не найдена</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: white;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        .error-section {{
            padding: 40px;
            text-align: center;
        }}
        .log-section {{
            background: rgba(0, 0, 0, 0.2);
            padding: 30px;
            border-top: 2px solid rgba(255, 255, 255, 0.1);
        }}
        .error-code {{
            font-size: 120px;
            font-weight: bold;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(0, 0, 0, 0.2);
            color: #ff6b6b;
        }}
        .error-title {{
            font-size: 36px;
            margin: 20px 0;
            color: #ffe66d;
        }}
        .error-info {{
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
            display: inline-block;
        }}
        .info-item {{
            margin: 5px 0;
            font-size: 16px;
        }}
        .log-title {{
            font-size: 24px;
            margin-bottom: 20px;
            color: #ffe66d;
            text-align: center;
        }}
        .log-entry {{
            background: rgba(255, 255, 255, 0.05);
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #4ecdc4;
        }}
        .log-ip {{
            font-weight: bold;
            color: #4ecdc4;
        }}
        .log-date {{
            color: #ffe66d;
            font-size: 14px;
        }}
        .log-url {{
            color: #ff6b6b;
            word-break: break-all;
        }}
        .log-agent {{
            color: #aaa;
            font-size: 12px;
            font-style: italic;
        }}
        .btn {{
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
        }}
        .btn:hover {{
            background: transparent;
            border-color: #4ecdc4;
            transform: translateY(-2px);
        }}
        .tea-cup {{
            font-size: 80px;
            margin: 20px 0;
            animation: bounce 2s infinite;
        }}
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .log-count {{
            text-align: center;
            margin-bottom: 15px;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error-section">
            <div class="tea-cup">☕</div>
            <h1 class="error-code">404</h1>
            <h2 class="error-title">Ой! Страница куда-то пропала</h2>
            
            <div class="error-info">
                <div class="info-item">🌐 <strong>Запрошенный URL:</strong> {requested_url}</div>
                <div class="info-item">📍 <strong>Ваш IP-адрес:</strong> {client_ip}</div>
                <div class="info-item">📅 <strong>Дата и время:</strong> {access_date}</div>
                <div class="info-item">🖥️ <strong>Браузер:</strong> {user_agent[:80]}...</div>
            </div>

            <div class="navigation">
                <a href="/" class="btn">🏠 На главную</a>
                <a href="/lab1" class="btn">📚 К лабораторным</a>
                <a href="javascript:history.back()" class="btn">↩️ Назад</a>
            </div>
        </div>
        
        <div class="log-section">
            <h3 class="log-title">📊 Журнал 404 ошибок</h3>
            <div class="log-count">Всего записей: {len(error_404_log)}</div>
            {log_html}
        </div>
    </div>
</body>
</html>
''', 404

@app.route("/400")
def badrequest():
    return '''
<!doctype html>
<html>
<head>
    <title>400 Bad Request </title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Неправильный, некорректный запрос.</p>
    <a href="/">На главную</a>
</body>
</html>
''', 400

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

# Лабораторная работа 2

flowers_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/a')
def lab2_a():
    return 'без слэша'

@app.route('/lab2/a/')
def lab2_a2():
    return 'со слешом'

@app.route('/lab2/flowers/<int:flower_id>')
def lab2_flowers(flower_id):
    if flower_id >= len(flowers_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
<head>
    <title>Цветок #{flower_id}</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
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
        <p><strong>Название:</strong> {flowers_list[flower_id]}</p>
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

@app.route('/lab2/add_flower/<name>')
def lab2_add_flower(name):
    flowers_list.append(name)
    return f'''
<!doctype html>
<html>
<head>
    <title>Цветок добавлен</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        .success-message {{
            background-color: #d4edda;
            color: #155724;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #28a745;
        }}
        .flower-list {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
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
    <h1>✅ Цветок успешно добавлен!</h1>
    
    <div class="success-message">
        <h2>Новый цветок: "{name}"</h2>
        <p>Цветок был добавлен в коллекцию.</p>
    </div>

    <div class="flower-list">
        <h3>📊 Статистика коллекции:</h3>
        <p><strong>Всего цветов:</strong> {len(flowers_list)}</p>
        <p><strong>Полный список:</strong> {', '.join(flowers_list)}</p>
    </div>

    <div class="navigation">
        <a href="/lab2/all_flowers" class="btn">📚 Посмотреть все цветы</a>
        <a href="/lab2/clear_flowers" class="btn">🗑️ Очистить коллекцию</a>
        <a href="/lab2" class="btn">🔙 К лабораторной 2</a>
        <a href="/" class="btn">🏠 На главную</a>
    </div>
</body>
</html>
'''

@app.route('/lab2/add_flower/')
def lab2_add_flower_empty():
    """Обработчик для случая, когда имя цветка не указано"""
    return '''
<!doctype html>
<html>
<head>
    <title>Ошибка добавления цветка</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 4px solid #dc3545;
        }
        .navigation {
            margin: 20px 0;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        .btn:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>❌ Ошибка добавления цветка</h1>
    
    <div class="error-message">
        <h2>400 - Неверный запрос</h2>
        <p><strong>Вы не задали имя цветка!</strong></p>
        <p>Пожалуйста, укажите название цветка в URL, например: <code>/lab2/add_flower/орхидея</code></p>
    </div>

    <div class="navigation">
        <a href="/lab2/all_flowers" class="btn">📚 Посмотреть все цветы</a>
        <a href="/lab2" class="btn">🔙 К лабораторной 2</a>
        <a href="/" class="btn">🏠 На главную</a>
    </div>
</body>
</html>
''', 400

@app.route('/lab2/all_flowers')
def lab2_all_flowers():
    """Роут для вывода всех цветов и их количества"""
    return render_template('all_flowers.html', flowers_list=flowers_list)

@app.route('/lab2/clear_flowers')
def lab2_clear_flowers():
    """Роут для очистки списка цветов"""
    flowers_list.clear()
    return '''
<!doctype html>
<html>
<head>
    <title>Коллекция очищена</title>
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">
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
        <a href="/lab2/add_flower/орхидея" class="btn btn-success">➕ Добавить первый цветок</a>
        <a href="/lab2" class="btn">🔙 К лабораторной 2</a>
        <a href="/" class="btn">🏠 На главную</a>
    </div>
</body>
</html>
'''

@app.route('/lab2/example')
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
    return render_template('example.html', 
                         name=name, 
                         number_lab=number_lab, 
                         number_course=number_course, 
                         number_group=number_group, 
                         fruits=fruits)

@app.route('/lab2/')
def lab2_index():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def lab2_filters():
    """Страница с демонстрацией фильтров"""
    phrase = "О сколько нам открытий чудных готовит просвещенья дух"
    return render_template('filters.html', phrase=phrase)

# Калькулятор
@app.route('/lab2/calc/')
def lab2_calc_default():
    """Перенаправление на калькулятор с значениями по умолчанию"""
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def lab2_calc_single(a):
    """Перенаправление на калькулятор с одним числом и вторым по умолчанию"""
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
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
    
    return render_template('calc.html', 
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

@app.route('/lab2/books')
def lab2_books():
    """Страница со списком книг"""
    return render_template('books.html', books=books_list)

# Список автомобилей
cars_list = [
    {
        'name': 'Tesla Model S',
        'image': 'tesla_model_s.jpg',
        'description': 'Электрический седан премиум-класса с автопилотом и ускорением 0-100 км/ч за 2.1 секунды'
    },
    {
        'name': 'BMW M5',
        'image': 'bmw_m5.jpg', 
        'description': 'Спортивный седан с двигателем V8 мощностью 600 л.с. и полным приводом xDrive'
    },
    {
        'name': 'Mercedes-Benz S-Class',
        'image': 'mercedes_s_class.jpg',
        'description': 'Флагманский седан люкс-класса с технологиями автономного вождения и роскошным салоном'
    },
    {
        'name': 'Audi RS6',
        'image': 'audi_rs6.jpg',
        'description': 'Универсал с двигателем V8 би-турбо мощностью 600 л.с. и спортивной подвеской'
    },
    {
        'name': 'Porsche 911',
        'image': 'porsche_911.jpg',
        'description': 'Легендарный спортивный автомобиль с задним расположением двигателя и уникальным дизайном'
    },
    {
        'name': 'Lamborghini Huracan',
        'image': 'lamborghini_huracan.jpg',
        'description': 'Суперкар с двигателем V10 мощностью 640 л.с. и агрессивным дизайном'
    },
    {
        'name': 'Ferrari F8 Tributo',
        'image': 'ferrari_f8.jpg',
        'description': 'Среднемоторный спорткар с двигателем V8 мощностью 720 л.с. и технологиями F1'
    },
    {
        'name': 'Rolls-Royce Phantom',
        'image': 'rolls_royce_phantom.jpg',
        'description': 'Ультра-люксовый седан ручной сборки с бесшумным салоном и индивидуальным интерьером'
    },
    {
        'name': 'Bentley Continental GT',
        'image': 'bentley_continental.jpg',
        'description': 'Гранд-турер с двигателем W12 и сочетанием роскоши с высокими динамическими характеристиками'
    },
    {
        'name': 'Ford Mustang',
        'image': 'ford_mustang.jpg',
        'description': 'Американский маслкар с двигателем V8 и культовым дизайном'
    },
    {
        'name': 'Chevrolet Corvette',
        'image': 'chevrolet_corvette.jpg',
        'description': 'Спортивный автомобиль с переднем расположением двигателя V8 и доступной ценой'
    },
    {
        'name': 'Jeep Wrangler',
        'image': 'jeep_wrangler.jpg',
        'description': 'Внедорожник с подключаемым полным приводом и съемными дверями для офф-роуда'
    },
    {
        'name': 'Land Rover Defender',
        'image': 'land_rover_defender.jpg',
        'description': 'Легендарный внедорожник с современными технологиями и выдающейся проходимостью'
    },
    {
        'name': 'Toyota Land Cruiser',
        'image': 'toyota_land_cruiser.jpg',
        'description': 'Надежный внедорожник с рамной конструкцией и репутацией неубиваемого автомобиля'
    },
    {
        'name': 'Volkswagen Golf GTI',
        'image': 'vw_golf_gti.jpg',
        'description': 'Хот-хэтч с богатой спортивной историей и отличной управляемостью'
    },
    {
        'name': 'Subaru WRX STI',
        'image': 'subaru_wrx.jpg',
        'description': 'Спортивный седан с оппозитным двигателем и симметричным полным приводом'
    },
    {
        'name': 'Nissan GT-R',
        'image': 'nissan_gtr.jpg',
        'description': 'Японский суперкар с двигателем V6 би-турбо и прозвищем "Бог"'
    },
    {
        'name': 'Mazda MX-5 Miata',
        'image': 'mazda_mx5.jpg',
        'description': 'Компактный родстер с идеальной развесовкой и доступной ценой для настоящего драйва'
    },
    {
        'name': 'Honda Civic Type R',
        'image': 'honda_civic_type_r.jpg',
        'description': 'Хот-хэтч с турбодвигателем и рекордом на Нюрбургринге среди переднеприводных автомобилей'
    },
    {
        'name': 'McLaren 720S',
        'image': 'mclaren_720s.jpg',
        'description': 'Суперкар с карбоновым монококом и двигателем V8 мощностью 720 л.с.'
    },
    {
        'name': 'Aston Martin DB11',
        'image': 'aston_martin_db11.jpg',
        'description': 'Гранд-турер с элегантным британским дизайном и двигателем от Mercedes-AMG'
    },
    {
        'name': 'Lexus LC 500',
        'image': 'lexus_lc500.jpg',
        'description': 'Купэ люкс-класса с атмосферным двигателем V8 и футуристичным дизайном'
    }
]

@app.route('/lab2/cars')
def lab2_cars():
    """Страница со списком автомобилей"""
    return render_template('cars.html', cars=cars_list)



if __name__ == '__main__':
    app.run(debug=False)