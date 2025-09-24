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

if __name__ == '__main__':
    app.run(debug=True)