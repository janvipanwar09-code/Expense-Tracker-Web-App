from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["expense_tracker"]
expenses_collection = db["expenses"]


@app.route("/")
def index():
    expenses = list(
        expenses_collection.find().sort("_id", -1)
    )

    total = sum(float(expense.get("amount", 0)) for expense in expenses)

    return render_template(
        "index.html",
        expenses=expenses,
        total=total
    )


@app.route("/add", methods=["POST"])
def add_expense():

    title = request.form["title"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    expenses_collection.insert_one({
        "title": title,
        "amount": amount,
        "category": category,
        "date": date
    })

    return redirect("/")


@app.route("/delete/<expense_id>")
def delete_expense(expense_id):

    expenses_collection.delete_one(
        {"_id": ObjectId(expense_id)}
    )

    return redirect("/")


@app.route("/edit/<expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):

    expense = expenses_collection.find_one(
        {"_id": ObjectId(expense_id)}
    )

    if request.method == "POST":

        title = request.form["title"]
        amount = float(request.form["amount"])
        category = request.form["category"]
        date = request.form["date"]

        expenses_collection.update_one(
            {"_id": ObjectId(expense_id)},
            {
                "$set": {
                    "title": title,
                    "amount": amount,
                    "category": category,
                    "date": date
                }
            }
        )

        return redirect("/")

    return render_template(
        "edit.html",
        expense=expense
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
   
   
  

  
