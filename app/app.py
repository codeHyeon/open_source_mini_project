from flask import Flask, render_template, request, redirect, url_for
from flasgger import Flasgger
from app.services.memo_service import MemoService

app = Flask(__name__)
flasgger = Flasgger(app)

memo_service = MemoService()

# ============== HTML TEST ==============
@app.route("/")
def index():
    """
    Render the main page with memo list.

    Retrieves all memos from the service layer and displays them on the index page.

    Returns:
        HTML: Rendered index page containing the memo list.
    """
    return render_template("index.html", memos=memo_service.get_memos())


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handle memo creation.

    - GET: Render the memo creation page.
    - POST: Save a new memo and redirect to the main page.

    Returns:
        HTML or Response: Rendered add page or redirect response.
    """
    if request.method == "POST":
        memo = request.form.get("memo")
        memo_service.add_memo(memo)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete")
def delete():
    """
    Render the memo deletion page.

    Displays the list of memos that can be deleted.

    Returns:
        HTML: Rendered delete page with memo list.
    """
    return render_template("delete.html", memos=memo_service.get_memos())


@app.route("/remove/<int:id>")
def remove(id):
    """
    Delete a memo by ID.

    Removes the specified memo and redirects to the delete page.

    Args:
        id (int): The ID of the memo to delete.

    Returns:
        Response: Redirect response to the delete page.
    """
    memo_service.delete_memo(id)
    return redirect(url_for("delete"))


@app.route("/detail/<int:id>")
def detail(id):
    """
    Display the detail page of a specific memo.

    Retrieves a single memo by its ID and displays it.

    Args:
        id (int): The ID of the memo to display.

    Returns:
        HTML: Rendered detail page with memo information.
    """
    memo = memo_service.get_memo(id)
    return render_template("detail.html", memo=memo)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    """
    Handle memo editing.

    - GET: Display the memo edit page.
    - POST: Update the memo and redirect to the main page.

    Args:
        id (int): The ID of the memo to edit.

    Returns:
        HTML or Response: Rendered edit page or redirect response.
    """
    memo = memo_service.get_memo(id)

    if request.method == "POST":
        content = request.form.get("memo")
        memo_service.update_memo(id, content)
        return redirect(url_for("index"))

    return render_template("edit.html", memo=memo)


@app.route("/api/memos", methods=["GET"])
def api_get_memos():
    """
    Get all memos.
    ---
    tags:
      - Memos
    responses:
      200:
        description: List of all memos
        schema:
          type: object
          properties:
            memos:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  content:
                    type: string
    """
    return {"memos": memo_service.get_memos()}

@app.route("/api/memos/<int:id>", methods=["GET"])
def api_get_memo(id):
    """
    Get a single memo by ID.
    ---
    tags:
      - Memos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the memo
    responses:
      200:
        description: Memo found
        schema:
          type: object
          properties:
            memo:
              type: object
              properties:
                id:
                  type: integer
                content:
                  type: string
      404:
        description: Memo not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    memo = memo_service.get_memo(id)
    if memo is None:
        return {"error": "not found"}, 404
    return {"memo": memo}, 200

@app.route("/api/memos", methods=["POST"])
def api_create_memo():
    """
    Create a new memo.
    ---
    tags:
      - Memos
    parameters:
      - name: memo
        in: formData
        type: string
        required: true
        description: The content of the memo
    responses:
      201:
        description: Memo created successfully
        schema:
          type: object
          properties:
            message:
              type: string
    """
    memo = request.form.get("memo")
    memo_service.add_memo(memo)
    return {"message": "created"}, 201

@app.route("/api/memos/<int:id>", methods=["PUT"])
def api_update_memo(id):
    """
    Update an existing memo.
    ---
    tags:
      - Memos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the memo to update
      - name: memo
        in: formData
        type: string
        required: true
        description: The new content for the memo
    responses:
      200:
        description: Memo updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Memo not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    memo = memo_service.get_memo(id)
    if memo is None:
        return {"error": "not found"}, 404

    content = request.form.get("memo")
    memo_service.update_memo(id, content)
    return {"message": "updated"}, 200

@app.route("/api/memos/<int:id>", methods=["DELETE"])
def api_delete_memo(id):
    """
    Delete a memo.
    ---
    tags:
      - Memos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: The ID of the memo to delete
    responses:
      200:
        description: Memo deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
      404:
        description: Memo not found
        schema:
          type: object
          properties:
            error:
              type: string
    """
    memo = memo_service.get_memo(id)
    if memo is None:
        return {"error": "not found"}, 404

    memo_service.delete_memo(id)
    return {"message": "deleted"}, 200


if __name__ == "__main__":
    app.run(debug=True)