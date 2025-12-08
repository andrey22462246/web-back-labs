from flask import Blueprint, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html', username='anonymous')

@lab8.route('/lab8/login')
def login():
    return render_template('lab8/login.html', username='anonymous')

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html', username='anonymous')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html', 
                              error='Имя пользователя не может быть пустым',
                              username='anonymous')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html', 
                              error='Пароль не может быть пустым',
                              username='anonymous')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                            error='Такой пользователь уже существует',
                            username='anonymous')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    flash('Регистрация успешна! Теперь вы можете войти.', 'success')
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
def show_articles():
    all_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/articles.html', articles=all_articles, username='anonymous')

@lab8.route('/lab8/create')
def create_article():
    return render_template('lab8/create.html', username='anonymous')