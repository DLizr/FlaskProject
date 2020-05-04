import threading

from flask import Flask, request, jsonify


__app = Flask(__name__)
__app.config["SECRET_KEY"] = "R@nd0m__Key"

players = dict()


@__app.route("/post/adduser", methods=["POST"])
def __adduser():
    senderIp = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if (senderIp != "127.0.0.1"):
        return jsonify({"error": "Unauthorized sender"})
    
    user = request.json["user"]
    players[user[0]] = user[1]
    return jsonify({"success": "ok"})


@__app.route("/post/shutdown", methods=["POST"])
def __shutdown():
    senderIp = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if (senderIp != "127.0.0.1"):
        return jsonify({"error": "Unauthorized sender"})
    
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return jsonify({"success": "ok"})


def __run():
    __app.run(port="5001")


__thread = threading.Thread(target=__run)
def run():
    __thread.start()


if __name__ == "__main__":
    run()
