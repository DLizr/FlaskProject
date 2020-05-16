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

global player_ids

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

env = app.jinja_env
env.add_extension("jinja2.ext.loopcontrols")

login_manager = LoginManager()
login_manager.init_app(app)
if not os.path.exists("db/blogs.sqlite"):
    os.mkdir("db")
    with open("db/blogs.sqlite", mode='w'):
        pass
player_ids = set()


def updateUsers(session):
    global users
    users = sorted(session.query(User).filter(User.banned_from_table == 0).all(), key=lambda x: -x.wins)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(news_api.blueprint)
    session = db_session.create_session()
    updateUsers(session)
    app.run(host="0.0.0.0", port=5000)


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
    news = session.query(News)
    return render_template("index.html", news=reversed([i for i in news]), users=users)


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
    if current_user.id in player_ids:
        return render_template('Error.html', number=403)

    player_ids.add(current_user.id)
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
    player_ids.remove(playerId)
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
    player_ids.remove(playerId)
    session = db_session.create_session()
    user = session.query(User).get(playerId)
    if (not user):
        return jsonify({"error": "Invalid user"}), 404

    user.gamesCount += 1
    user.wins += 1
    session.commit()
    updateUsers(session)

    return jsonify({"success": "ok"})


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
    return render_template("about.html", news=reversed([i for i in news]))


@app.errorhandler(404)
def not_found(error):
    session = db_session.create_session()
    news = session.query(News)
    return render_template('Error.html', error='404 не найден: запрошенный URL-адрес не был найден'
                                               ' на сервере. Если вы ввели URL вручную, пожалуйста,'
                                               ' проверьте орфографию и повторите попытку.',
                           news=reversed([i for i in news]))


@app.errorhandler(403)
def forbidden(error):
    session = db_session.create_session()
    news = session.query(News)
    return render_template('Error.html', error='Ошибка 403 запрещено:'
                                               ' доступ к странице или ресурсу,'
                                               ' который вы пытались открыть,'
                                               ' по какой-то причине абсолютно запрещен.',
                           news=reversed([i for i in news]))


@app.errorhandler(500)
def internal_error(error):
    session = db_session.create_session()
    news = session.query(News)
    return render_template('Error.html', error='Внутренняя ошибка сервера 500: '
                                               'что что-то пошло не так на сервере веб-сайта,'
                                               ' но сервер не может более конкретно сообщить'
                                               ' о том, в чем именно заключается проблема.',
                           news=reversed([i for i in news]))


@app.errorhandler(401)
def unauthorized(error):
    session = db_session.create_session()
    news = session.query(News)
    return render_template('Error.html', error='401 не авторизован:'
                                               ' сервер не смог проверить,'
                                               ' что вы авторизованы для доступа'
                                               ' к запрошенному URL-адресу.'
                                               ' Вы либо ввели неверные учетные данные '
                                               '(например, неверный пароль), '
                                               'либо ваш браузер не понимает, '
                                               'как предоставить необходимые'
                                               ' учетные данные.', news=reversed([i for i in news]))


if __name__ == '__main__':
    main()
