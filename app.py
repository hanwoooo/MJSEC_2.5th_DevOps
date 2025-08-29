# from flask import Flask, render_template, request, redirect

# app = Flask(__name__)

# # 임시 데이터 저장
# messages = []

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         name = request.form.get("name", "익명")
#         text = request.form.get("message", "")
#         if text.strip():
#             messages.append({"name": name, "message": text})
#         return redirect("/")
#     return render_template("index.html", messages=messages)

# @app.route("/dd")
# def dd():
#     return render_template("dd.html")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)

from flask import (
    Flask, abort, request, render_template,
    redirect, url_for, make_response
)
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)

# flags.json 로드
with open('flags.json', 'r', encoding='utf-8') as f:
    FLAGS = json.load(f)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    code = getattr(e, 'code', None)
    if code and 400 <= code < 500:
        return FLAGS[str(code)], code
    return e

@app.route("/")
def index():
    return '''
HTTP응답코드 중 400번대를 발생시키면, 플래그가 출력됩니다. 해당 플래그를 구글 폼에 적어주세요.<br>소스코드: https://github.com/MJSEC-MJU/Welcome_MJSEC-3rd<br>힌트: 소스코드를 확인해보세요!
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username != 'admin' or password != 'secret':
            error = '잘못된 아이디 또는 비밀번호'
            return render_template('login.html', error=error)
        # 로그인 성공 시
        resp = make_response(redirect(url_for('mjsec')))
        # 쿠키 설정: 이름 hidden_key, 값 MJSEC_secret, 1시간 유효, HttpOnly
        resp.set_cookie('hidden_key', 'MJSEC_secret',
                        max_age=3600, httponly=True)
        return resp

    return render_template('login.html', error=error)

@app.route('/mjsec')
def mjsec():
    # 쿠키에서 'hidden_key' 값 꺼내기.
    key = request.cookies.get('hidden_key', '')
    if key != 'MJSEC_secret':
        abort(403)
    return render_template('mjsec.html')

@app.route('/admin', methods=['POST'])
def admin():
    key = request.form.get('hidden_key', '')
    if key != 'MJSEC_secret':
        abort(401)
    return render_template('mjsec.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
