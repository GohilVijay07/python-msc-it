
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, "todo.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Task Model
class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    priority = db.Column(db.String(20), default="Medium")
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)


# Create database table automatically
with app.app_context():
    db.create_all()


# Home: Show all tasks
@app.route("/")
def index():
    pending_tasks = Task.query.filter_by(
        is_completed=False
    ).order_by(Task.id.desc()).all()

    completed_tasks = Task.query.filter_by(
        is_completed=True
    ).order_by(Task.id.desc()).all()

    return render_template(
        "index.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        total=len(pending_tasks) + len(completed_tasks),
        pending_count=len(pending_tasks),
        completed_count=len(completed_tasks)
    )


# Add Task
@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Medium").strip()
    due_date_text = request.form.get("due_date", "").strip()

    if title:
        due_date = None

        if due_date_text:
            try:
                due_date = datetime.strptime(
                    due_date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                due_date = None

        if priority not in ["High", "Medium", "Low"]:
            priority = "Medium"

        task = Task(
            title=title,
            description=description or None,
            priority=priority,
            due_date=due_date,
            is_completed=False
        )

        db.session.add(task)
        db.session.commit()

    return redirect(url_for("index"))


# Mark Task Completed or Pending
@app.route("/toggle/<int:id>")
def toggle_task(id):
    task = db.session.get(Task, id)

    if task:
        task.is_completed = not task.is_completed
        db.session.commit()

    return redirect(url_for("index"))


# Update Task
# Supports normal HTML forms (POST) and API requests (PUT)
@app.route("/update/<int:id>", methods=["POST", "PUT"])
@app.route("/edit/<int:id>", methods=["POST", "PUT"])
def update_task(id):
    task = db.session.get(Task, id)

    if task:
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium").strip()
        due_date_text = request.form.get("due_date", "").strip()

        if title:
            task.title = title

        task.description = description or None

        if priority in ["High", "Medium", "Low"]:
            task.priority = priority

        if due_date_text:
            try:
                task.due_date = datetime.strptime(
                    due_date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                task.due_date = None
        else:
            task.due_date = None

        db.session.commit()

    return redirect(url_for("index"))


# Delete Task
# Supports normal HTML forms (POST) and API requests (DELETE)
@app.route("/delete/<int:id>", methods=["POST", "DELETE"])
def delete_task(id):
    task = db.session.get(Task, id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for("index"))


# Delete all completed tasks
@app.route("/clear-completed", methods=["POST"])
def clear_completed():
    Task.query.filter_by(is_completed=True).delete()
    db.session.commit()

    return redirect(url_for("index"))


# Run locally
if __name__ == "__main__":
    app.run(debug=True)
