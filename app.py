from flask import Flask, render_template, request, redirect, url_for
from services.memo_service import MemoService

app = Flask(__name__)

memo_service = MemoService()

@app.route("/")
def index():
    return render_template("index.html", memos=memo_service.get_memos())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        memo = request.form.get("memo")
        memo_service.add_memo(memo)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete")
def delete():
    return render_template("delete.html", memos=memo_service.get_memos())


@app.route("/remove/<int:id>")
def remove(id):
    memo_service.delete_memo(id)
    return redirect(url_for("delete"))


if __name__ == "__main__":
    app.run(debug=True)