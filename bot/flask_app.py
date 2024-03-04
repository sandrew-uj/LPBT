from flask import Flask, render_template, request, send_file

app = Flask(__name__)
# REQ_URL = "http://127.0.0.1:8000" # testing
# REQ_URL = "http://172.16.30.4:6555"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
