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
@app.route("/lab1/")  # ДОБАВИЛ ЭТУ СТРОКУ!
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
    return "нет такой страницы", 404
@app.route("/400")
def bad_request():
    return '''
<!doctype html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за клиентской ошибки (неправильный синтаксис, неверный запрос и т.д.)</p>
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
if __name__ == '__main__':
    app.run(debug=True)