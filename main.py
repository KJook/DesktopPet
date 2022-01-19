from flask import Flask, jsonify, request
from util.window import root, gs, playMeow
from PyQt5.QtWidgets import QApplication
import sys
import threading
from util.edit import delWebSite, addWebSite
import json

flask_app = Flask(__name__)

def retrun_template(code = 0, state='ok', data='', error=''):
    return jsonify({
            "code": code,
            "state": state,
            "data": data,
            "error": error
        })


@flask_app.route("/api/say", methods=['POST'])
def say():
    post_str=request.form['str']
    try:
        gs.print.emit(post_str)
        meow_thread = threading.Thread(target=playMeow())
        meow_thread.setDaemon(True)
        meow_thread.start()
        return retrun_template()
    except Exception as e:
        return retrun_template(1, state='bad request', error=str(e))

@flask_app.route("/api/clear", methods=['POST'])
def clear():
    try:
        gs.clear.emit()
        return retrun_template()

    except Exception as e:
        return retrun_template(1, state='bad request', error=str(e))



@flask_app.route("/api/get_conf", methods=['POST'])
def get_conf():
    try:
        with open('conf.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return retrun_template(0, data=data)
    except Exception as e:
        return retrun_template(1, state='bad request', error=str(e))


@flask_app.route("/api/web_del", methods=['POST'])
def website():
    post_str=request.form['title']
    try:
        if delWebSite(post_str) == 0:
            return retrun_template()
        else:
            return retrun_template(2, state='Not Found', error="Can not found %s" % post_str)
    except Exception as e:
        return retrun_template(1, state='bad request', error=str(e))


@flask_app.route("/api/web_add", methods=['POST'])
def website2():
    post_str_title=request.form['title']
    post_str_url=request.form['url']
    try:
        addWebSite(post_str_title, post_str_url)
        return retrun_template()
    except Exception as e:
        return retrun_template(1, state='bad request', error=str(e))


def app_run():
    flask_app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = root()
    app_thread = threading.Thread(target=app_run)
    app_thread.setDaemon(True)
    app_thread.start()
    sys.exit(app.exec_())

