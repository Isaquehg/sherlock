# flask --app app run
from flask import Flask, render_template
from database import Database
from queries import Query

app = Flask(__name__)
db = Database("bolt://44.197.243.30:7687", "neo4j", "funding-tablet-motion")
sherlock = Query(db)

@app.route("/home")
def home():
    case_numbers = sherlock.get_cases_all()
    return render_template('index.html', case_numbers=case_numbers)

@app.route('/home/<case_number>')
def case_details(case_number):
    case = sherlock.get_case(case_number)

    return render_template('case_details.html', case_number=case_number)