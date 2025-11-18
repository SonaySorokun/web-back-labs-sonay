from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'knowledge_base_db',
            user='sonay_sorokun_knowledge_base',
            password='123a'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method =='GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT login FROM users WHERE login=?;", (login, ))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error='Такой пользователь уже существует')
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute(f"INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    conn.commit()
    db_close(conn, cur)
    return render_template('lab5/success.html',
                            login=login)


@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method =='GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html',
                            login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute(f"SELECT * FROM users WHERE login=?;", (login, ))
    user_id = cur.fetchone()['id']


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"INSERT INTO articles(user_id, title, article_text)\
                      VALUES (%s, %s, %s);", (user_id, title, article_text))
    else:
        cur.execute(f"INSERT INTO articles(login_id, title, article_text)\
                      VALUES (?, ?, ?);", (user_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list', methods=['GET'])
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT * FROM articles WHERE user_id = %s;", (user_id, ))
    else:
        cur.execute(f"SELECT * FROM articles WHERE login_id = ?;", (user_id, ))

    articles = cur.fetchall()


    db_close(conn, cur)

    if not articles:
        return render_template('lab5/articles.html', error='Статьи отсутствуют')
    else:
        return render_template('lab5/articles.html', articles=articles)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return render_template('lab5/lab5.html')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id = ?;", (article_id,))
        
        article = cur.fetchone()
        db_close(conn, cur)
        
        if not article:
            return "Статья не найдена", 404
            
        return render_template('lab5/edit.html', article=article)

    new_title = request.form.get('new_title')
    new_article_text = request.form.get('new_article_text')

    if not new_title or not new_article_text:
        return render_template('lab5/edit.html', error='Поля не могут быть пустыми', article=article)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title = %s, article_text = %s WHERE id = %s AND user_id = %s;", 
                   (new_title, new_article_text, article_id, user_id))
    else:
        cur.execute("UPDATE articles SET title = ?, article_text = ? WHERE id = ? AND login_id = ?;", 
                   (new_title, new_article_text, article_id, user_id))
    
    db_close(conn, cur)

    return redirect('/lab5/list')


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"SELECT id FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute(f"SELECT id FROM users WHERE login = ?;", (login, ))

    user_id = cur.fetchone()['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(f"DELETE FROM articles WHERE user_id = %s AND id = %s;", (user_id, article_id))
    else:
        cur.execute(f"DELETE FROM articles WHERE login_id = ? AND id = ?;", (user_id, article_id))

    db_close(conn, cur)

    return redirect('/lab5/list')