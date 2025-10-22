from flask import Blueprint, url_for, request, redirect, abort
import datetime

lab1 = Blueprint('lab1',__name__)

@lab1.route("/lab1")
@lab1.route("/lab1/")
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

@lab1.route("/lab1/web")
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

@lab1.route("/lab1/author")
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

@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="lab1/oak.jpg")
    css_path = url_for("static", filename="lab1/lab1.css")
    
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

@lab1.route("/lab1/counter")
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

@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/created")
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



