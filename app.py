from flask import Flask, jsonify, request
from window import *
import sys

flask_app = Flask(__name__)

@flask_app.route("/api/say", methods=['POST'])
def say():
    post_str=request.form['str']
    try:
        gs.print.emit(post_str)
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

def app_run():
    flask_app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    graph = root()
    app_thread = threading.Thread(target=app_run)
    app_thread.setDaemon(True)
    app_thread.start()
    sys.exit(app.exec_())

