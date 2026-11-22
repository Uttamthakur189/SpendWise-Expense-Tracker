from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        t_type = request.form['type']
        category = request.form['category']
        date = datetime.now().strftime('%Y-%m-%d')

        c.execute('INSERT INTO transactions (title, amount, type, category, date) VALUES (?, ?, ?, ?, ?)',
                  (title, amount, t_type, category, date))
        conn.commit()
        return redirect(url_for('index'))

    c.execute('SELECT * FROM transactions ORDER BY id DESC')
    transactions = c.fetchall()

    total_income = sum(t[2] for t in transactions if t[3] == 'Income')
    total_expense = sum(t[2] for t in transactions if t[3] == 'Expense')
    balance = total_income - total_expense

    conn.close()
    return render_template('index.html', transactions=transactions, 
                           income=total_income, expense=total_expense, balance=balance)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
