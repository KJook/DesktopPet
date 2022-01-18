from flask import Flask, jsonify, request
from util.window import root, gs, playMeow
from PyQt5.QtWidgets import QApplication
import sys
import threading
from util.edit import delWebSite, addWebSite

flask_app = Flask(__name__)

@flask_app.route("/api/say", methods=['POST'])
def say():
    post_str=request.form['str']
    try:
        gs.print.emit(post_str)
        meow_thread = threading.Thread(target=playMeow())
        meow_thread.setDaemon(True)
        meow_thread.start()
        return jsonify({
            "code": 0,
            "state": "ok"
        })
    except Exception as e:
        return jsonify({
            "code": 1,
            "state": "bad_request",
            "error": str(e)
        })

@flask_app.route("/api/clear", methods=['POST'])
def clear():
    try:
        gs.clear.emit()
        return jsonify({
            "code": 0,
            "state": "ok"
        })
    except Exception as e:
        return jsonify({
            "code": 1,
            "state": "bad_request",
            "error": str(e)
        })

@flask_app.route("/api/web_del", methods=['POST'])
def website():
    post_str=request.form['title']
    try:
        if delWebSite(post_str) == 0:
            return jsonify({
                "code": 0,
                "state": "ok"
            })
        else:
            return jsonify({
                "code": 2,
                "state": "%s not exits" % (post_str)
            })
    except Exception as e:
        return jsonify({
            "code": 1,
            "state": "bad_request",
            "error": str(e)
        })


@flask_app.route("/api/web_add", methods=['POST'])
def website2():
    post_str_title=request.form['title']
    post_str_url=request.form['url']
    try:
        addWebSite(post_str_title, post_str_url)
        return jsonify({
                "code": 0,
                "state": "ok"
            })
    except Exception as e:
        return jsonify({
            "code": 1,
            "state": "bad_request",
            "error": str(e)
        })


def app_run():
    flask_app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = root()
    app_thread = threading.Thread(target=app_run)
    app_thread.setDaemon(True)
    app_thread.start()
    sys.exit(app.exec_())

