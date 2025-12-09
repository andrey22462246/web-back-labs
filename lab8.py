from flask import Blueprint, render_template, request, redirect, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, current_user, login_required
from sqlalchemy import or_, func

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    
    public_articles = articles.query.filter_by(is_public=True).limit(5).all()
    
    return render_template('lab8/lab8.html', 
                          username=username,
                          public_articles=public_articles)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/login.html', username=username)
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')

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
            remember = True if remember_me == 'on' else False
            login_user(user, remember=remember)
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
    
    login_user(new_user, remember=False)
    
    flash(f'Регистрация успешна! Добро пожаловать, {login_form}!', 'success')
    return redirect('/lab8/')

@lab8.route('/lab8/articles')
def show_articles():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    search_query = request.args.get('search', '').strip()
    
    query = articles.query
    
    if current_user.is_authenticated:
        query = query.filter(
            (articles.is_public == True) | (articles.login_id == current_user.id)
        )
    else:
        query = query.filter_by(is_public=True)
    
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                func.lower(articles.title).like(func.lower(search_pattern)),
                func.lower(articles.article_text).like(func.lower(search_pattern))
            )
        )
    
    all_articles = query.all()
    
    for article in all_articles:
        article.author_name = users.query.get(article.login_id).login if users.query.get(article.login_id) else 'Неизвестен'
        article.is_owner = current_user.is_authenticated and article.login_id == current_user.id
    
    return render_template('lab8/articles.html', 
                          articles=all_articles, 
                          username=username,
                          show_all_public=True,
                          search_query=search_query)

@lab8.route('/lab8/my_articles')
@login_required
def my_articles():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    search_query = request.args.get('search', '').strip()
    
    query = articles.query.filter_by(login_id=current_user.id)
    
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            or_(
                func.lower(articles.title).like(func.lower(search_pattern)),
                func.lower(articles.article_text).like(func.lower(search_pattern))
            )
        )
    
    user_articles = query.all()
    
    for article in user_articles:
        article.is_owner = True
    
    return render_template('lab8/articles.html', 
                          articles=user_articles, 
                          username=username,
                          show_all_public=False,
                          search_query=search_query)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/create.html', username=username)
    
    title = request.form.get('title')
    article_text = request.form.get('content')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/create.html',
                              error='Заголовок статьи не может быть пустым',
                              username=username)
    
    if not article_text or not article_text.strip():
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/create.html',
                              error='Текст статьи не может быть пустым',
                              username=username)
    
    new_article = articles(
        login_id=current_user.id,
        title=title.strip(),
        article_text=article_text.strip(),
        is_favorite=is_favorite,
        is_public=is_public
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    flash(f'Статья "{title.strip()}" успешно создана!', 'success')
    return redirect('/lab8/my_articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        abort(403)
    
    if request.method == 'GET':
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/edit.html', 
                             article=article, 
                             username=username)
    
    title = request.form.get('title')
    article_text = request.form.get('content')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not title.strip():
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/edit.html',
                              error='Заголовок статьи не может быть пустым',
                              article=article,
                              username=username)
    
    if not article_text or not article_text.strip():
        username = current_user.login if current_user.is_authenticated else 'anonymous'
        return render_template('lab8/edit.html',
                              error='Текст статьи не может быть пустым',
                              article=article,
                              username=username)
    
    article.title = title.strip()
    article.article_text = article_text.strip()
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    flash(f'Статья "{title.strip()}" успешно обновлена!', 'success')
    return redirect('/lab8/my_articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        abort(403)
    
    db.session.delete(article)
    db.session.commit()
    
    flash(f'Статья "{article.title}" удалена!', 'success')
    return redirect('/lab8/my_articles')

@lab8.route('/lab8/logout')
@login_required
def logout():
    from flask_login import logout_user
    logout_user()
    return redirect('/lab8/')