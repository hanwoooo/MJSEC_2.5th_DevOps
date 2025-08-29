from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 임시 데이터 저장
messages = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "익명")
        text = request.form.get("message", "")
        if text.strip():
            messages.append({"name": name, "message": text})
        return redirect("/")
    return render_template("index.html", messages=messages)

@app.route("/dd")
def dd():
    return render_template("dd.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
