from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

todoapp = Flask(__name__, template_folder="templates")
todoapp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
todoapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(todoapp)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

# Create all database tables within an application context
with todoapp.app_context():
    db.create_all()

@todoapp.route("/")
def index():
    todos = Todo.query.all()
    return render_template("base.html", todos=todos)

@todoapp.route("/add", methods=["POST"])
def add():
    todo_text = request.form['todo']
    new_todo = Todo(task=todo_text)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@todoapp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.task = request.form["todo"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo)

@todoapp.route("/check/<int:id>")
def check(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))

@todoapp.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    todoapp.run(debug=True)
