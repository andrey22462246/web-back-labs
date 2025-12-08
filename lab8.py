from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, current_user, login_required

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/login.html', username=username)
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/login.html',
                              error='Имя пользователя не может быть пустым',
                              username=username)

    if not password_form or password_form.strip() == '':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/login.html',
                              error='Пароль не может быть пустым',
                              username=username)

    user = users.query.filter_by(login=login_form).first()
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect('/lab8/')

    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны',
                           username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/register.html', username=username)

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/register.html', 
                              error='Имя пользователя не может быть пустым',
                              username=username)

    if not password_form or password_form.strip() == '':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/register.html', 
                              error='Пароль не может быть пустым',
                              username=username)

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/register.html', 
                            error='Такой пользователь уже существует',
                            username=username)
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Регистрация успешна! Теперь вы можете войти.', 'success')
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
@login_required
def show_articles():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return "список статей"

@lab8.route('/lab8/create')
def create_article():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/create.html', username=username)