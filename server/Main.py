import datetime
import os

from flask import Flask, render_template, request, make_response, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from data import db_session, news_api
from data.LoginForm import LoginForm
from data.NewsForm import NewsForm
from data.RegisterForm import RegisterForm
from data.news import News

from data.users import User
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
if not os.path.exists("db/blogs.sqlite"):
    os.mkdir("db")
    with open("db/blogs.sqlite", mode='w'):
        pass

def main():
    global users
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(news_api.blueprint)
    session = db_session.create_session()
    con = sqlite3.connect("db/blogs.sqlite")
    cur = con.cursor()
    users = [i for i in sorted(cur.execute("""SELECT * FROM users""").fetchall(), key=lambda x: x[-1])][::-1]
    app.run()


@app.route('/favicon.img')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.img',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(News)
    return render_template("index.html", news=reversed([i for i in news]), users=users)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", users=users)
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", users=users)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, users=users)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, users=users)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form, users=users)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        news = session.query(News).filter(News.id == id,
                                          News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Редактирование новости', form=form, users=users)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    session = db_session.create_session()
    news = session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        session.delete(news)
        session.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/game")
@login_required
def game():
    return render_template("game.html")


@app.route("/content/<int:id>")
def content(id):
    session = db_session.create_session()
    ids = [i.id for i in session.query(News)]
    if id not in ids:
        return redirect('/404')
    new = session.query(News).filter(News.id == id).first()
    news = session.query(News)
    return render_template("right.html", new=new, count=len([i for i in session.query(News)]), news=news)

@app.route("/about")
def about():
    session = db_session.create_session()
    news = session.query(News)
    return render_template("about.html", news=news)

@app.errorhandler(404)
def not_found(error):
    return render_template('Error.html', number=error)


if __name__ == '__main__':
    main()
