from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

memos = []

@app.route("/")
def index():
    return render_template("index.html", memos=memos)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        memo = request.form.get("memo")
        memos.append(memo)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete")
def delete():
    return render_template("delete.html", memos=memos)


@app.route("/remove/<int:id>")
def remove(id):
    if 0 <= id < len(memos):
        memos.pop(id)

    return redirect(url_for("delete"))


if __name__ == "__main__":
    app.run(debug=True)