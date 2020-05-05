import threading
import requests

from flask import Flask, request, jsonify, abort

from src.util.Logger import logger


__app = Flask(__name__)
__app.config["SECRET_KEY"] = "R@nd0m__Key"

players = dict()


def localhostOnly(func):
    def localhostOnlyRoute(*args, **kwargs):
        senderIp = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        if (senderIp != "127.0.0.1"):
            return jsonify({"error": "Unauthorized sender"}), 403
        
        return func(*args, **kwargs)
    localhostOnlyRoute.__name__ = func.__name__
    return localhostOnlyRoute


@__app.route("/post/adduser", methods=["POST"])
@localhostOnly
def __adduser():
    user = request.json["user"]
    players[user[0]] = user[1]
    return jsonify({"success": "ok"})


@__app.route("/post/shutdown", methods=["POST"])
@localhostOnly
def __shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return jsonify({"success": "ok"})


def addWin(playerId: int):
    code = requests.post("http://localhost:5000/post/addwin/{}".format(playerId)).status_code
    if (code != 200):
        logger.error("Unable to find a user with id {}. Game is not counted.".format(playerId))


def addGame(playerId: int):
    code = requests.post("http://localhost:5000/post/addgame/{}".format(playerId)).status_code
    if (code != 200):
        logger.error("Unable to find a user with id {}. Game is not counted.".format(playerId))


def __run():
    __app.run(port="5001")


__thread = threading.Thread(target=__run)
def run():
    __thread.start()


if __name__ == "__main__":
    run()
