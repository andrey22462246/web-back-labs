from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime
import sqlite3

lab7 = Blueprint('lab7',__name__)

def get_db_connection():
    conn = sqlite3.connect('films.db')
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    
    films_list = []
    for film in films:
        films_list.append(dict_from_row(film))
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if film:
        return jsonify(dict_from_row(film))
    else:
        abort(404)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
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

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
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

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
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