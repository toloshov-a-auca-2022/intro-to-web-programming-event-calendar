from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events ORDER BY date')
    events = c.fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']

        conn = sqlite3.connect('events.db')
        c = conn.cursor()
        c.execute('INSERT INTO events (title, date, description) VALUES (?, ?, ?)', (title, date, description))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add_event.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
