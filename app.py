from flask import Flask, render_template, request, jsonify, redirect, url_for
import calendar
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Configure your database URI
db = SQLAlchemy(app)

# --- Database Models ---
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    goal = db.Column(db.String(120))
    # Add user relationship if needed

class HabitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    # Add user relationship if needed

with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/calendar')
def show_calendar():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    cal_html = calendar.HTMLCalendar().formatmonth(year, month)
    return render_template('calendar.html', calendar_html=cal_html)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_habit', methods=['POST'])
def add_habit():
    data = request.get_json()
    name = data.get('habitName')
    goal = data.get('habitGoal')
    if name:
        new_habit = Habit(name=name, goal=goal)
        db.session.add(new_habit)
        db.session.commit()
        return jsonify({'message': 'Habit added successfully', 'habit': {'id': new_habit.id, 'name': new_habit.name, 'goal': new_habit.goal}}), 201
    return jsonify({'error': 'Habit name is required'}), 400

@app.route('/get_habits')
def get_habits():
    habits = Habit.query.all()
    habit_list = [{'id': h.id, 'name': h.name, 'goal': h.goal} for h in habits]
    return jsonify(habit_list)

@app.route('/mark_habit_done', methods=['POST'])
def mark_habit_done():
    data = request.get_json()
    habit_id = data.get('habitId')
    date_str = data.get('date')
    completed = data.get('completed', True)
    try:
        log_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    existing_log = HabitLog.query.filter_by(habit_id=habit_id, date=log_date).first()
    if existing_log:
        return jsonify({'message': 'Habit already marked for this day'}), 200

    habit_log = HabitLog(habit_id=habit_id, date=log_date, completed=completed)
    db.session.add(habit_log)
    db.session.commit()
    return jsonify({'message': 'Habit marked as done for this day'}), 201

# --- Authentication Routes ---
users = { "shiv": "3" }

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username in users and users[username] == password:
        return redirect(url_for('welcome', username=username))
    else:
        return "Login failed! Invalid username or password."

@app.route('/welcome/<username>')
def welcome(username):
    return f"Welcome, {username}! 🎉 You are logged into Habit Hero!"

if __name__ == '__main__':
    app.run(debug=True)


  #from flask import Flask, render_template, request, redirect, url_for
'''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  
app = Flask(__name__)

# pip install flask_sqlalchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search')
    if search_query:
        habits = Habit.query.filter(Habit.name.contains(search_query)).all()
    else:
        habits = Habit.query.all()
    return render_template('index.html', habits=habits)

@app.route('/add', methods=['POST'])
def add_habit():
    name = request.form.get('name')
    description = request.form.get('description')
    if name and description:
        new_habit = Habit(name=name, description=description)
        db.session.add(new_habit)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        db.session.delete(habit)
        db.session.commit()
    return redirect('/')

@app.route('/edit/<int:habit_id>')
def edit_habit(habit_id):
    habit = Habit.query.get(habit_id)
    return render_template('edit.html', habit=habit)

@app.route('/update/<int:habit_id>', methods=['POST'])
def update_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        habit.name = request.form.get('name')
        habit.description = request.form.get('description')
        db.session.commit()
    return redirect('/')

@app.route('/complete/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if habit:
        habit.completed = not habit.completed  # Toggle complete status
        db.session.commit()
    return redirect('/')

@app.route('/')
def home():
    return "Hello! Welcome to Localhost 5001"

if __name__ == '__main__':
    app.run(port=5001)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

  '''