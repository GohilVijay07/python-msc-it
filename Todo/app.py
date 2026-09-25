import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite Database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ---------------------------------------------------------------------------
# Data Schema / Model: Task
# ---------------------------------------------------------------------------
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)                      # Primary key
    title = db.Column(db.String(150), nullable=False)                 # Task title
    description = db.Column(db.String(300), nullable=True)            # Details about the task
    priority = db.Column(db.String(20), default='Medium')             # "High", "Medium", "Low"
    is_completed = db.Column(db.Boolean, default=False)               # True / False
    due_date = db.Column(db.Date, nullable=True)                      # Task deadline (Date)

    def __repr__(self):
        return f"<Task #{self.id}: {self.title} [{self.priority}] (Completed: {self.is_completed})>"

# Alias for backward compatibility
Todo = Task


# Helper: Seed initial sample tasks
def seed_sample_data():
    if Task.query.count() == 0:
        samples = [
            Task(
                title="Complete Python Assignment",
                description="Complete Flask practical with database CRUD operations",
                priority="High",
                is_completed=False,
                due_date=date(2026, 9, 25)
            ),
            Task(
                title="Prepare Semester Project Presentation",
                description="Create slides covering database schema and architecture",
                priority="Medium",
                is_completed=False,
                due_date=date(2026, 9, 28)
            ),
            Task(
                title="Review Lecture Notes on SQLAlchemy",
                description="Revise models, queries, and session commit methods",
                priority="Low",
                is_completed=True,
                due_date=date(2026, 9, 24)
            ),
        ]
        db.session.add_all(samples)
        db.session.commit()


# ---------------------------------------------------------------------------
# Routes & Functionality
# ---------------------------------------------------------------------------

# 1. GET / : Display two sections: Pending Tasks and Completed Tasks
@app.route('/')
def index():
    # Order pending tasks by priority/due date, completed tasks by id descending
    pending_tasks = Task.query.filter_by(is_completed=False).order_by(Task.id.desc()).all()
    completed_tasks = Task.query.filter_by(is_completed=True).order_by(Task.id.desc()).all()
    
    total = len(pending_tasks) + len(completed_tasks)
    completed_count = len(completed_tasks)
    pending_count = len(pending_tasks)

    return render_template(
        'index.html',
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        total=total,
        completed_count=completed_count,
        pending_count=pending_count
    )


# 2. POST /add : Form to add a new task with title, description, priority, and due date
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip() or None
    priority = request.form.get('priority', 'Medium').strip()
    due_date_str = request.form.get('due_date', '').strip()

    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            due_date = None

    if title:
        new_task = Task(
            title=title,
            description=description,
            priority=priority if priority in ['High', 'Medium', 'Low'] else 'Medium',
            due_date=due_date,
            is_completed=False
        )
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('index'))


# 3. GET /toggle/<id> : One-click button to toggle a task between Pending and Completed
@app.route('/toggle/<int:id>')
def toggle_task(id):
    task = db.session.get(Task, id)
    if task:
        task.is_completed = not task.is_completed
        db.session.commit()

    return redirect(url_for('index'))


# 4. POST /update/<id> : Update the details of an existing task
@app.route('/update/<int:id>', methods=['PUT'])
@app.route('/edit/<int:id>', methods=['PUT'])  # Alias for backward compatibility
def update_task(id):
    task = db.session.get(Task, id)
    if task:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip() or None
        priority = request.form.get('priority', 'Medium').strip()
        due_date_str = request.form.get('due_date', '').strip()

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            except ValueError:
                due_date = None

        if title:
            task.title = title
        task.description = description
        if priority in ['High', 'Medium', 'Low']:
            task.priority = priority
        task.due_date = due_date

        db.session.commit()

    return redirect(url_for('index'))


# 5. POST /delete/<id> : Remove a task from the to-do list
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = db.session.get(Task, id)
    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for('index'))


# Optional Helper: Clear all completed tasks
@app.route('/clear-completed', methods=['POST', 'GET'])
def clear_completed():
    Task.query.filter_by(is_completed=True).delete()
    db.session.commit()
    return redirect(url_for('index'))


# ---------------------------------------------------------------------------
# App Entrypoint
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_sample_data()
    app.run(debug=True)