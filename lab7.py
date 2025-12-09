import os
import sqlite3
from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

def init_db():
    """Инициализация базы данных, если её нет"""
    try:
        base_dir = '/home/andrey2246/web-back-labs/'
        db_path = os.path.join(base_dir, 'films.db')
        
        print(f"DEBUG init_db: Проверяем путь {db_path}")
        print(f"DEBUG init_db: Файл существует: {os.path.exists(db_path)}")
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films';")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("DEBUG init_db: Таблица 'films' не существует, создаём...")
            cursor.execute('''
                CREATE TABLE films (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    title_ru TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    description TEXT NOT NULL
                )
            ''')
            print("DEBUG init_db: Таблица 'films' создана")
            
            
            cursor.execute("SELECT COUNT(*) FROM films")
            count = cursor.fetchone()[0]
            if count == 0:
                print("DEBUG init_db: Добавляем тестовые данные...")
                test_data = [
                    ('The Shawshank Redemption', 'Побег из Шоушенка', 1994, 'Драма о жизни в тюрьме'),
                    ('The Godfather', 'Крестный отец', 1972, 'Криминальная драма о мафии'),
                    ('The Dark Knight', 'Темный рыцарь', 2008, 'Боевик о Бэтмене и Джокере')
                ]
                cursor.executemany('''
                    INSERT INTO films (title, title_ru, year, description) 
                    VALUES (?, ?, ?, ?)
                ''', test_data)
                print(f"DEBUG init_db: Добавлено {len(test_data)} тестовых фильмов")
        else:
            print("DEBUG init_db: Таблица 'films' уже существует")
        
        conn.commit()
        
        
        cursor.execute("SELECT COUNT(*) FROM films")
        count = cursor.fetchone()[0]
        print(f"DEBUG init_db: Всего фильмов в базе: {count}")
        
        conn.close()
        print("DEBUG init_db: База данных инициализирована")
        
    except Exception as e:
        print(f"ERROR init_db: Ошибка при инициализации БД: {str(e)}")
        raise

def get_db_connection():
    try:
        base_dir = '/home/andrey2246/web-back-labs/'
        db_path = os.path.join(base_dir, 'films.db')
        
        print(f"DEBUG get_db_connection: Путь: {db_path}")
        print(f"DEBUG get_db_connection: Файл существует: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            print(f"ERROR get_db_connection: Файл БД не найден по пути {db_path}")
            raise FileNotFoundError(f"Файл БД не найден: {db_path}")
        
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films';")
        if not cursor.fetchone():
            print("ERROR get_db_connection: Таблица 'films' не существует в БД")
            conn.close()
            raise Exception("Таблица 'films' не существует в базе данных")
        
        return conn
        
    except Exception as e:
        print(f"ERROR get_db_connection: {str(e)}")
        raise

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    try:
        print("DEBUG get_films: Начало получения фильмов")
        conn = get_db_connection()
        
       
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(films);")
        columns = cursor.fetchall()
        print(f"DEBUG get_films: Структура таблицы: {columns}")
        
        films = conn.execute('SELECT * FROM films').fetchall()
        conn.close()
        
        print(f"DEBUG get_films: Получено {len(films)} фильмов")
        
        films_list = []
        for film in films:
            films_list.append(dict_from_row(film))
        
        print(f"DEBUG get_films: Возвращаем JSON с {len(films_list)} фильмами")
        return jsonify(films_list)
        
    except FileNotFoundError as e:
        print(f"ERROR get_films: Файл БД не найден: {str(e)}")
        return jsonify({"error": "Database file not found"}), 500
    except Exception as e:
        print(f"ERROR get_films: Ошибка: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    try:
        conn = get_db_connection()
        film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        if film:
            return jsonify(dict_from_row(film))
        else:
            abort(404)
    except Exception as e:
        print(f"Ошибка при получении фильма {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@lab7.route('/lab7/debug/db')
def debug_db():
    """Маршрут для отладки базы данных"""
    try:
        base_dir = '/home/andrey2246/web-back-labs/'
        db_path = os.path.join(base_dir, 'films.db')
        
        info = {
            "db_path": db_path,
            "file_exists": os.path.exists(db_path),
            "file_size": os.path.getsize(db_path) if os.path.exists(db_path) else 0,
            "error": None
        }
        
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            info["tables"] = [row[0] for row in cursor.fetchall()]
            
            
            cursor.execute("PRAGMA table_info(films);")
            info["films_structure"] = cursor.fetchall()
            
            
            cursor.execute("SELECT COUNT(*) FROM films;")
            info["films_count"] = cursor.fetchone()[0]
            
            
            cursor.execute("SELECT * FROM films LIMIT 5;")
            info["films_sample"] = cursor.fetchall()
            
            conn.close()
        
        return jsonify(info)
        
    except Exception as e:
        info["error"] = str(e)
        return jsonify(info), 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    try:
        conn = get_db_connection()
        film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
        
        if film:
            conn.execute('DELETE FROM films WHERE id = ?', (id,))
            conn.commit()
            conn.close()
            return '', 204
        else:
            conn.close()
            abort(404)
    except Exception as e:
        print(f"Ошибка при удалении фильма {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    try:
        conn = get_db_connection()
        film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
        
        if not film:
            conn.close()
            abort(404)
        
        data = request.get_json()
        
        errors = {}
        
        if not data.get('title_ru') or data['title_ru'].strip() == '':
            errors['title_ru'] = 'Русское название не может быть пустым'
        
        if not data.get('title') or data['title'].strip() == '':
            errors['title'] = 'Оригинальное название не может быть пустым'
        
        if data.get('title_ru') and (not data.get('title') or data['title'].strip() == ''):
            data['title'] = data['title_ru']
        
        if not data.get('year'):
            errors['year'] = 'Год не может быть пустым'
        else:
            try:
                year = int(data['year'])
                current_year = datetime.now().year
                if year < 1895 or year > current_year:
                    errors['year'] = f'Год должен быть от 1895 до {current_year}'
            except:
                errors['year'] = 'Год должен быть числом'
        
        if not data.get('description') or data['description'].strip() == '':
            errors['description'] = 'Описание не может быть пустым'
        elif len(data['description']) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
        
        if errors:
            conn.close()
            return jsonify(errors), 400
        
        conn.execute('''
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ? 
            WHERE id = ?
        ''', (data['title'], data['title_ru'], data['year'], data['description'], id))
        
        conn.commit()
        
        updated_film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
        conn.close()
        
        return jsonify(dict_from_row(updated_film))
    except Exception as e:
        print(f"Ошибка при обновлении фильма {id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    try:
        data = request.get_json()
        
        errors = {}
        
        if not data.get('title_ru') or data['title_ru'].strip() == '':
            errors['title_ru'] = 'Русское название не может быть пустым'
        
        if not data.get('title') or data['title'].strip() == '':
            errors['title'] = 'Оригинальное название не может быть пустым'
        
        if data.get('title_ru') and (not data.get('title') or data['title'].strip() == ''):
            data['title'] = data['title_ru']
        
        if not data.get('year'):
            errors['year'] = 'Год не может быть пустым'
        else:
            try:
                year = int(data['year'])
                current_year = datetime.now().year
                if year < 1895 or year > current_year:
                    errors['year'] = f'Год должен быть от 1895 до {current_year}'
            except:
                errors['year'] = 'Год должен быть числом'
        
        if not data.get('description') or data['description'].strip() == '':
            errors['description'] = 'Описание не может быть пустым'
        elif len(data['description']) > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
        
        if errors:
            return jsonify(errors), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (?, ?, ?, ?)
        ''', (data['title'], data['title_ru'], data['year'], data['description']))
        
        film_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({"id": film_id}), 201
    except Exception as e:
        print(f"Ошибка при добавлении фильма: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


init_db()