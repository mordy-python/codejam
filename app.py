from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TodoItem(db.Model):
    def __init__(self, title, content, duedate):
        self.title = title
        self.duedate = duedate
        self.content = content
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    duedate = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.title} is due on {self.duedate}"
class Event(db.Model):
    def __init__(self, event_type, date, notes):
        self.event_type = event_type
        self.date = date
        self.notes = notes
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f"{self.event_type} {self.date} {self.notes}"
@app.route("/")
def home():
    data = TodoItem.query.all()
    return render_template('index.html', title='Home', header='Dashboard', date=date.today(), due=data)
@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'GET':
        list1 = TodoItem.query.all()
        list1 = list1[::-1]
        if len(list1) == 0:
            content = [{'title':'Nothing to do! Click the plus to add tasks', 'content':'All your tasks are done', 'duedate':'Nothing is due'}]
        else:
            content = list1
        return render_template('todo.html', content=content, title="Todo List", header='Todo List')
    else:
        title = request.form.get('title')
        description = request.form.get('description')
        ddate = request.form.get('due_date')
        todo = TodoItem(title, description, ddate)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo', methods=['GET']))
@app.route("/todo/del/<id>")
def del_id(id):
    id = TodoItem.query.get(id)
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('todo'))
@app.route("/dates-and-times", methods=['GET', 'POST'])
def dat():
    if request.method == 'GET':
        events = Event.query.all()
        events = events[::-1]
        return render_template('dat.html', header="Important Dates and Times", dates=events)
    else:
        e_type = request.form.get('type')
        date = request.form.get('date')
        notes = request.form.get('notes')
        event = Event(e_type, date, notes)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('dat', methods=['GET']))
@app.route("/del/event/<id>")
def del_event(id):
    id = Event.query.get(id)
    db.session.delete(id)
    db.session.commit()
    return redirect(url_for('dat'))
if __name__ == "__main__":
    db.create_all() # creates all the tables in the db
    app.run(debug=True, port='8000')
