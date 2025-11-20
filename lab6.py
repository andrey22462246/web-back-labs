from flask import Blueprint, render_template, request, redirect, session
import sqlite3

lab6 = Blueprint('lab6',__name__)

def get_db_connection():
    """Подключение к существующей SQLite базе данных"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Unauthorized'},
            'id': id
        }
    
    if data['method'] == 'info':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM offices ORDER BY number')
            offices = cursor.fetchall()
            conn.close()
            
            offices_list = []
            for office in offices:
                offices_list.append({
                    'number': office['number'],
                    'tenant': office['tenant'],
                    'price': office['price']
                })
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Database error: {str(e)}'},
                'id': id
            }
    
    elif data['method'] == 'booking':
        office_number = data['params']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
            office = cursor.fetchone()
            
            if not office:
                conn.close()
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': -32000, 'message': 'Office not found'},
                    'id': id
                }
            
            if office['tenant']:
                conn.close()
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 2, 'message': 'Already booked'},
                    'id': id
                }
            
            cursor.execute('UPDATE offices SET tenant = ? WHERE number = ?', 
                         (login, office_number))
            conn.commit()
            conn.close()
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Database error: {str(e)}'},
                'id': id
            }

    elif data['method'] == 'release':
        office_number = data['params']
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM offices WHERE number = ?', (office_number,))
            office = cursor.fetchone()
            
            if not office:
                conn.close()
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': -32000, 'message': 'Office not found'},
                    'id': id
                }
            
            if not office['tenant']:
                conn.close()
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 3, 'message': 'Office is not booked'},
                    'id': id
                }
            
            if office['tenant'] != login:
                conn.close()
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 4, 'message': 'You can only release your own booking'},
                    'id': id
                }
            
            cursor.execute('UPDATE offices SET tenant = ? WHERE number = ?', 
                         ('', office_number))
            conn.commit()
            conn.close()
            
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Database error: {str(e)}'},
                'id': id
            }

    elif data['method'] == 'my_offices':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM offices WHERE tenant = ?', (login,))
            user_offices = cursor.fetchall()
            conn.close()
            
            total_cost = sum(office['price'] for office in user_offices)
            
            return {
                'jsonrpc': '2.0',
                'result': {
                    'offices': [dict(office) for office in user_offices],
                    'total_cost': total_cost,
                    'count': len(user_offices)
                },
                'id': id
            }
        except Exception as e:
            return {
                'jsonrpc': '2.0',
                'error': {'code': -32000, 'message': f'Database error: {str(e)}'},
                'id': id
            }