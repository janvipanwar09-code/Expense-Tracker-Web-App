from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "expenses.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


@app.route("/")
def index():
    connection = get_db_connection()

    expenses = connection.execute(
        "SELECT * FROM expenses ORDER BY date DESC"
    ).fetchall()

    total = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/add", methods=["POST"])
def add_expense():

    title = request.form["title"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO expenses (title, amount, category, date)
        VALUES (?, ?, ?, ?)
        """,
        (title, amount, category, date)
    )

    connection.commit()
    connection.close()

    return redirect("/")


@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):

    connection = get_db_connection()

    connection.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    connection.commit()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
