from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
import datetime
import math
import os 
from dotenv import load_dotenv

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "секретно-секретный секрет")
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

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
    <link rel="icon" type="image/x-icon" href="/static/lab2/favicon.ico">
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
            <li><a href="/lab3">🍪 Лабораторная работа 3</a></li>
            <li><a href="/lab4">📪 Лабораторная работа 4</a></li>
            <li><a href="/lab5">🛢️ Лабораторная работа 5</a></li>
            <li><a href="/lab6">😃 Лабораторная работа 6</a></li>
            <li><a href="/lab7">😴 Лабораторная работа 7</a></li>
            <li><a href="/lab8">📝 Лабораторная работа 8</a></li>        
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

        <div class="lab-card lab3">
            <h3>🍪 Лабораторная работа 3</h3>
            <p>Формы(GET), cookie</p>
            <a href="/lab3">Перейти к лабораторной →</a>
        </div>

        <div class="lab-card lab4">
            <h3>📪 Лабораторная работа 4</h3>
            <p>Формы(POST)</p>
            <a href="/lab4">Перейти к лабораторной →</a>
        </div>

        <div class="lab-card lab5">
            <h3>🛢️ Лабораторная работа 5</h3>
            <p>Flask и БД</p>
            <a href="/lab5">Перейти к лабораторной →</a>
        </div>

        <div class="lab-card lab6">
            <h3>😃 Лабораторная работа 6</h3>
            <p>API JSON-RPC</p>
            <a href="/lab6">Перейти к лабораторной →</a>
        </div>

        <div class="lab-card lab7">
            <h3>😴 Лабораторная работа 7</h3>
            <p>API REST</p>
            <a href="/lab7">Перейти к лабораторной →</a>
        </div>

        <div class="lab-card lab8">
            <h3>📝 Лабораторная работа 8</h3>
            <p>Flask и ORM</p>
            <a href="/lab8">Перейти к лабораторной →</a>
        </div>
    </div>
    
    <footer>
        <p>Шкуропатов Андрей Александрович, ФБИ-32, 3 курс, {current_year} год</p>
    </footer>
</body>
</html>
'''

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
    <link rel="icon" type="image/x-icon" href="/static/lab2/favicon.ico">
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