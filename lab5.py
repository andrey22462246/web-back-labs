from flask import Blueprint, render_template

lab5 = Blueprint('lab5',__name__)

@lab5.route('/lab5/')
def main():
    return render_template('lab5/lab5.html')

@lab5.route('/login')
def login():
    return render_template('lab5/login.html')

@lab5.route('/register')
def register():
    return render_template('lab5/register.html')

@lab5.route('/list')
def list_articles():
    return render_template('lab5/list.html')

@lab5.route('/create')
def create_article():
    return render_template('lab5/create.html')