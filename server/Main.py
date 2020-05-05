import datetime
import os
import random
import requests

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)
if not os.path.exists("db/blogs.sqlite"):
    os.mkdir("db")
    with open("db/blogs.sqlite", mode='w'):
        pass


def updateUsers(session):
    global users
    users = sorted(session.query(User).filter(User.banned_from_table == 0).all(), key=lambda x: -x.wins)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(news_api.blueprint)
    session = db_session.create_session()
    updateUsers(session)
    app.run()


@app.route('/stealth/<int:id>')
def stealthbutton(id):
    if current_user.is_authenticated != 1:
        return render_template('Error.html', number=403)
    if current_user.is_admin == 0:
        return render_template('Error.html', number=403)
    session = db_session.create_session()
    banned = session.query(User).filter(User.id == id).first()
    banned.banned_from_table = 1
    session.commit()
    updateUsers(session)
    return redirect('/')


@app.route('/favicon.img')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.img',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
def index():
    session = db_session.create_session()
    # news = session.query(News).filter(News.is_private != True)
    news = session.query(News)
    res = make_response(render_template("index.html", news=news))
    res.set_cookie("visits_count", '1', max_age=60 * 60 * 24 * 365 * 2)
    return render_template("index.html", news=news, users=users)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if current_user.is_authenticated == 1:
        return render_template('Error.html', number=403)
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
        updateUsers(session)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, users=users)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/session_test/')
def session_test():
    if 'visits_count' in session:
        session['visits_count'] = session.get('visits_count') + 1
    else:
        session['visits_count'] = 1
    # дальше - код для вывода страницы


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == 1:
        return render_template('Error.html', number=403)
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
    if current_user.is_authenticated != 1:
        return render_template('Error.html', number=403)
    if current_user.is_admin == 0:
        return render_template('Error.html', number=403)
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
    if current_user.is_authenticated != 1:
        return render_template('Error.html', number=403)
    if current_user.is_admin == 0:
        return render_template('Error.html', number=403)
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
    if current_user.is_authenticated != 1:
        return render_template('Error.html', number=403)
    if current_user.is_admin == 0:
        return render_template('Error.html', number=403)
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
    code = str(random.randint(0, 2 ** 32))
    requests.post("http://localhost:5001/post/adduser", json={"user": [code, current_user.id]})
    return render_template("game.html", code=code)


def localhostOnly(func):
    def localhostOnlyRoute(*args, **kwargs):
        senderIp = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if (senderIp != "127.0.0.1"):
            return jsonify({"error": "Unauthorized sender"}), 403
        
        return func(*args, **kwargs)
    localhostOnlyRoute.__name__ = func.__name__
    return localhostOnlyRoute


@app.route("/post/addgame/<int:playerId>", methods=["POST"])
@localhostOnly
def addGame(playerId):
    session = db_session.create_session()
    user = session.query(User).get(playerId)
    if (not user):
        return jsonify({"error": "Invalid user"}), 404
    
    user.gamesCount += 1
    session.commit()
    
    return jsonify({"success": "ok"})


@app.route("/post/addwin/<int:playerId>", methods=["POST"])
@localhostOnly
def addWin(playerId):
    session = db_session.create_session()
    user = session.query(User).get(playerId)
    if (not user):
        return jsonify({"error": "Invalid user"}), 404
    
    user.gamesCount += 1
    user.wins += 1
    session.commit()
    updateUsers(session)
    
    return jsonify({"success": "ok"})


@app.errorhandler(404)
def not_found(error):
    return render_template('Error.html', number=error)


if __name__ == '__main__':
    main()
