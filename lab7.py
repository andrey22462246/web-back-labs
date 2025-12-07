import os
import sqlite3
from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

def init_db():
    """Инициализация базы данных, если её нет"""
    base_dir = '/home/andrey2246/web-back-labs/'
    db_path = os.path.join(base_dir, 'films.db')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("DEBUG: Таблица 'films' создана или уже существует")

def get_db_connection():
    base_dir = '/home/andrey2246/web-back-labs/'
    db_path = os.path.join(base_dir, 'films.db')
    
    print(f"DEBUG: Подключаюсь к БД по пути: {db_path}")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    try:
        conn = get_db_connection()
        films = conn.execute('SELECT * FROM films').fetchall()
        conn.close()
        
        films_list = []
        for film in films:
            films_list.append(dict_from_row(film))
        return jsonify(films_list)
    except Exception as e:
        print(f"Ошибка при получении фильмов: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

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