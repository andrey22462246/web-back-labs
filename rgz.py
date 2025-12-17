from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import re
from functools import wraps

# Создаем Blueprint для РГЗ
rgz = Blueprint('rgz', __name__, url_prefix='/rgz')

# Настройки
DB_NAME = 'rgz_database.db'

# ========== УТИЛИТЫ БАЗЫ ДАННЫХ ==========
def init_db():
    """Инициализация базы данных для РГЗ"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rgz_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        about TEXT,
        avatar TEXT DEFAULT '👤',
        is_admin INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        group_name TEXT DEFAULT 'ФБИ-32'
    )
    ''')
    
    # Таблица объявлений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rgz_advertisements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES rgz_users (id)
    )
    ''')
    
    # Добавляем колонку avatar, если её нет (для существующих БД)
    try:
        cursor.execute("SELECT avatar FROM rgz_users LIMIT 1")
    except sqlite3.OperationalError:
        # Колонки нет - добавляем
        cursor.execute("ALTER TABLE rgz_users ADD COLUMN avatar TEXT DEFAULT '👤'")
        print("Добавлена колонка avatar в таблицу пользователей")
    
    conn.commit()
    
    # Создаем администратора
    cursor.execute('SELECT * FROM rgz_users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        hashed_password = hashlib.sha256('Admin123!'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO rgz_users (username, password, full_name, email, avatar, is_admin) VALUES (?, ?, ?, ?, ?, ?)',
            ('admin', hashed_password, 'Администратор', 'admin@example.com', '👑', 1)
        )
        print("Создан администратор: admin / Admin123!")
    
    # Создаем тестового пользователя
    cursor.execute('SELECT * FROM rgz_users WHERE username = ?', ('test1',))
    if not cursor.fetchone():
        hashed_password = hashlib.sha256('password123'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO rgz_users (username, password, full_name, email, avatar) VALUES (?, ?, ?, ?, ?)',
            ('test1', hashed_password, 'Тестовый Пользователь', 'test1@example.com', '😎')
        )
        print("Создан тестовый пользователь: test1 / password123")
    
    # Создаем тестового студента
    cursor.execute('SELECT * FROM rgz_users WHERE username = ?', ('student',))
    if not cursor.fetchone():
        hashed_password = hashlib.sha256('Student123!'.encode()).hexdigest()
        cursor.execute(
            'INSERT INTO rgz_users (username, password, full_name, email, avatar) VALUES (?, ?, ?, ?, ?)',
            ('student', hashed_password, 'Студент ФБИ-32', 'student@example.com', '🎓')
        )
        print("Создан тестовый студент: student / Student123!")
    
    conn.commit()
    conn.close()
    print("База данных РГЗ инициализирована")

def get_db():
    """Получение соединения с БД"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ========== ВАЛИДАЦИЯ ==========
def validate_username(username):
    if not username or len(username) < 3:
        return "Имя пользователя должно содержать минимум 3 символа"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return "Имя пользователя может содержать только латинские буквы, цифры и подчеркивание"
    return None

def validate_password(password):
    if len(password) < 6:
        return "Пароль должен содержать минимум 6 символов"
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+=\-\[\]{};\':"\\|,.<>\/?]+$', password):
        return "Пароль содержит недопустимые символы"
    return None

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return "Некорректный формат email"
    return None

def validate_ad(title, content):
    if not title or len(title.strip()) < 3:
        return "Заголовок должен содержать минимум 3 символа"
    if not content or len(content.strip()) < 10:
        return "Текст объявления должен содержать минимум 10 символов"
    return None

# ========== ДЕКОРАТОРЫ ==========
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rgz_user_id' not in session:
            flash('Требуется авторизация', 'error')
            return redirect(url_for('rgz.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rgz_user_id' not in session:
            flash('Требуется авторизация', 'error')
            return redirect(url_for('rgz.login'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT is_admin FROM rgz_users WHERE id = ?', (session['rgz_user_id'],))
        user = cursor.fetchone()
        conn.close()
        
        if not user or not user['is_admin']:
            flash('Доступ запрещен. Требуются права администратора', 'error')
            return redirect(url_for('rgz.index'))
        
        return f(*args, **kwargs)
    return decorated_function

# ========== МОДЕЛИ ==========
class UserModel:
    @staticmethod
    def create(username, password, full_name, email, avatar='👤', about=None):
        conn = get_db()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            cursor.execute(
                'INSERT INTO rgz_users (username, password, full_name, email, avatar, about) VALUES (?, ?, ?, ?, ?, ?)',
                (username, hashed_password, full_name, email, avatar, about)
            )
            conn.commit()
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError as e:
            conn.close()
            raise e
        finally:
            conn.close()
        
        return user_id
    
    @staticmethod
    def get_by_username(username):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rgz_users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM rgz_users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user
    
    @staticmethod
    def verify_password(stored_password, provided_password):
        return stored_password == hashlib.sha256(provided_password.encode()).hexdigest()
    
    @staticmethod
    def delete(user_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rgz_users WHERE id = ?', (user_id,))
        cursor.execute('DELETE FROM rgz_advertisements WHERE author_id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, full_name, email, avatar, is_admin, created_at FROM rgz_users ORDER BY created_at DESC')
        users = cursor.fetchall()
        conn.close()
        return users

class AdvertisementModel:
    @staticmethod
    def create(title, content, author_id):
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO rgz_advertisements (title, content, author_id) VALUES (?, ?, ?)',
            (title, content, author_id)
        )
        conn.commit()
        ad_id = cursor.lastrowid
        conn.close()
        return ad_id
    
    @staticmethod
    def get_all():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, u.username, u.full_name, u.email, u.avatar, u.group_name 
            FROM rgz_advertisements a 
            JOIN rgz_users u ON a.author_id = u.id 
            ORDER BY a.created_at DESC
        ''')
        ads = cursor.fetchall()
        conn.close()
        return ads
    
    @staticmethod
    def get_by_id(ad_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, u.username, u.full_name, u.email, u.avatar, u.group_name 
            FROM rgz_advertisements a 
            JOIN rgz_users u ON a.author_id = u.id 
            WHERE a.id = ?
        ''', (ad_id,))
        ad = cursor.fetchone()
        conn.close()
        return ad
    
    @staticmethod
    def update(ad_id, title, content):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE rgz_advertisements SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
            (title, content, ad_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(ad_id):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM rgz_advertisements WHERE id = ?', (ad_id,))
        conn.commit()
        conn.close()

# ========== МАРШРУТЫ ==========
@rgz.route('/')
def index():
    """Главная страница доски объявлений"""
    init_db()
    ads = AdvertisementModel.get_all()
    
    # Проверяем, находится ли пользователь в сессии РГЗ
    user_id = session.get('rgz_user_id')
    username = session.get('rgz_username')
    is_admin = session.get('rgz_is_admin')
    avatar = session.get('rgz_avatar')
    
    return render_template('rgz/index.html', 
                         ads=ads, 
                         user_id=user_id,
                         username=username,
                         is_admin=is_admin,
                         avatar=avatar)

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = UserModel.get_by_username(username)
        if user and UserModel.verify_password(user['password'], password):
            # Используем префикс rgz_ для сессии, чтобы не конфликтовать с лабами
            session['rgz_user_id'] = user['id']
            session['rgz_username'] = user['username']
            session['rgz_is_admin'] = user['is_admin']
            session['rgz_avatar'] = user['avatar']
            flash('Вход выполнен успешно', 'success')
            return redirect(url_for('rgz.index'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')
    
    return render_template('rgz/login.html')

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        avatar = request.form.get('avatar', '👤')
        about = request.form.get('about', '')
        
        # Если выбрана кастомная аватарка
        custom_avatar = request.form.get('avatar_custom', '')
        if custom_avatar:
            avatar = custom_avatar
        
        # Валидация
        if error := validate_username(username):
            flash(error, 'error')
        elif error := validate_password(password):
            flash(error, 'error')
        elif error := validate_email(email):
            flash(error, 'error')
        elif not full_name or len(full_name.strip()) < 2:
            flash('Введите корректное имя', 'error')
        elif UserModel.get_by_username(username):
            flash('Пользователь с таким именем уже существует', 'error')
        else:
            try:
                UserModel.create(username, password, full_name, email, avatar, about)
                flash('Регистрация прошла успешно. Теперь вы можете войти.', 'success')
                return redirect(url_for('rgz.login'))
            except Exception as e:
                flash(f'Ошибка при регистрации: {str(e)}', 'error')
    
    # Список доступных эмоджи для аватарок
    emojis = ['👤', '😎', '🎓', '🧑‍💻', '👨‍🎓', '👩‍🎓', '🤓', '😊', '😄', '🌟', '🔥', '💫', '🐱', '🐶', '🦊', '🐼', '🦁', '🐯']
    
    return render_template('rgz/register.html', emojis=emojis)

@rgz.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('rgz_user_id', None)
    session.pop('rgz_username', None)
    session.pop('rgz_is_admin', None)
    session.pop('rgz_avatar', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('rgz.index'))

@rgz.route('/create', methods=['GET', 'POST'])
@login_required
def create_ad():
    """Создание объявления"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if error := validate_ad(title, content):
            flash(error, 'error')
        else:
            AdvertisementModel.create(title, content, session['rgz_user_id'])
            flash('Объявление успешно создано', 'success')
            return redirect(url_for('rgz.index'))
    
    return render_template('rgz/create_ad.html')

@rgz.route('/edit/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    """Редактирование объявления"""
    ad = AdvertisementModel.get_by_id(ad_id)
    
    if not ad:
        flash('Объявление не найдено', 'error')
        return redirect(url_for('rgz.index'))
    
    # Проверка прав доступа
    if ad['author_id'] != session['rgz_user_id'] and not session.get('rgz_is_admin'):
        flash('У вас нет прав для редактирования этого объявления', 'error')
        return redirect(url_for('rgz.index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if error := validate_ad(title, content):
            flash(error, 'error')
        else:
            AdvertisementModel.update(ad_id, title, content)
            flash('Объявление успешно обновлено', 'success')
            return redirect(url_for('rgz.index'))
    
    return render_template('rgz/edit_ad.html', ad=ad)

@rgz.route('/delete/<int:ad_id>')
@login_required
def delete_ad(ad_id):
    """Удаление объявления"""
    ad = AdvertisementModel.get_by_id(ad_id)
    
    if not ad:
        flash('Объявление не найдено', 'error')
        return redirect(url_for('rgz.index'))
    
    # Проверка прав доступа
    if ad['author_id'] != session['rgz_user_id'] and not session.get('rgz_is_admin'):
        flash('У вас нет прав для удаления этого объявления', 'error')
        return redirect(url_for('rgz.index'))
    
    AdvertisementModel.delete(ad_id)
    flash('Объявление удалено', 'success')
    return redirect(url_for('rgz.index'))

@rgz.route('/delete_account')
@login_required
def delete_account():
    """Удаление аккаунта пользователя"""
    if session.get('rgz_is_admin'):
        flash('Аккаунт администратора нельзя удалить', 'error')
        return redirect(url_for('rgz.index'))
    
    user_id = session['rgz_user_id']
    
    # Очищаем сессию
    session.pop('rgz_user_id', None)
    session.pop('rgz_username', None)
    session.pop('rgz_is_admin', None)
    session.pop('rgz_avatar', None)
    
    # Удаляем пользователя
    UserModel.delete(user_id)
    flash('Ваш аккаунт успешно удален', 'info')
    return redirect(url_for('rgz.index'))

@rgz.route('/admin')
@admin_required
def admin_panel():
    """Панель администратора"""
    users = UserModel.get_all()
    ads = AdvertisementModel.get_all()
    return render_template('rgz/admin.html', users=users, ads=ads)

@rgz.route('/admin/delete_user/<int:user_id>')
@admin_required
def delete_user(user_id):
    """Удаление пользователя администратором"""
    if user_id == session['rgz_user_id']:
        flash('Нельзя удалить собственный аккаунт', 'error')
    else:
        UserModel.delete(user_id)
        flash('Пользователь удален', 'success')
    return redirect(url_for('rgz.admin_panel'))

# Инициализация БД при импорте
init_db()

# Добавляем тестовые объявления
def add_test_ads():
    conn = get_db()
    cursor = conn.cursor()
    
    # Проверяем, есть ли уже объявления
    cursor.execute('SELECT COUNT(*) FROM rgz_advertisements')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Получаем ID пользователей
        cursor.execute('SELECT id FROM rgz_users WHERE username = "admin"')
        admin_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM rgz_users WHERE username = "test1"')
        test1_id = cursor.fetchone()[0]
        
        cursor.execute('SELECT id FROM rgz_users WHERE username = "student"')
        student_id = cursor.fetchone()[0]
        
        # Добавляем тестовые объявления
        test_ads = [
            ('Продаю ноутбук', 'Отличный ноутбук в идеальном состоянии. Процессор i7, 16 ГБ ОЗУ, SSD 512 ГБ. Цена договорная.', test1_id),
            ('Ищу репетитора по математике', 'Нужен репетитор для студента 1 курса. Занятия 2 раза в неделю.', student_id),
            ('Сдам комнату в общежитии', 'Свободная комната в общежитии №5. Все удобства, недалеко от метро.', test1_id),
            ('Куплю учебники по программированию', 'Ищу учебники по Python, Flask и базам данных. Готов забрать в любой день.', student_id),
            ('Помощь с лабораторными по вебу', 'Готов помочь с выполнением лабораторных работ по веб-программированию.', admin_id),
        ]
        
        for title, content, author_id in test_ads:
            cursor.execute(
                'INSERT INTO rgz_advertisements (title, content, author_id) VALUES (?, ?, ?)',
                (title, content, author_id)
            )
        
        conn.commit()
        print("Тестовые объявления добавлены!")
    
    conn.close()

# Добавляем тестовые объявления при запуске
add_test_ads()