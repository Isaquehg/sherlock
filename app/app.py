# flask --app app run
from flask import Flask, redirect, render_template, request
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
    data = sherlock.get_case(case_number)
    # Extracting Case
    case = data[0]
    # Extracting Suspects
    suspects = data[1]
    # Extracting Victims
    victims = data[2]
    # Extracting Investigators
    investigators = data[3]
    # Extracting Evidences
    evidences = data[4]

    return render_template('case_details.html', case=case, suspects=suspects, victims=victims, investigators=investigators, evidences=evidences)

@app.route('/create/case')
def create_case():
    if request.method == 'POST':
        case_number = request.form.get('case_number')
        description = request.form.get('description')
        status = request.form.get('status')

        # Save the form data to the database using your database functions
        sherlock.create_case(case_number, description, status)

        # Redirect to a success page or the case details page
        return redirect('/home/{}'.format(case_number))
    else:
        return render_template('create_case.html')
    
@app.route('/create/suspect')
def create_suspect():
    if request.method == 'POST':
        suspect_name = request.form.get('name')
        suspect_alias = request.form.get('alias')
        suspect_date_of_birth = request.form.get('date_of_birth')
        suspect_description = request.form.get('description')
        suspect_case_number = request.form.get('case_number')

        # Save the form data to the database and assign to the case
        sherlock.create_suspect(suspect_name, suspect_alias, suspect_date_of_birth, suspect_description)
        sherlock.involved_in(suspect_case_number, suspect_name)

        # Redirect to a success page or the case details page
        return redirect('/home/{}'.format(suspect_case_number))
    else:
        return render_template('create_suspect.html')
    
@app.route('/create/victim')
def create_victim():
    if request.method == 'POST':
        victim_name = request.form.get('victim_name')
        victim_age = request.form.get('age')
        victim_contact_information = request.form.get('contact_information')
        victim_case_number = request.form.get('case_number')

        # Save the form data to the database and assign to the case
        sherlock.create_suspect(victim_name, victim_age, victim_contact_information)
        sherlock.affected(victim_case_number, victim_name)

        # Redirect to a success page or the case details page
        return redirect('/home/{}'.format(victim_case_number))
    else:
        return render_template('create_victim.html')
    
@app.route('/create/investigator')
def create_investigator():
    if request.method == 'POST':
        investigator_badge_number = request.form.get('investigator_badge')
        investigator_name = request.form.get('name')
        investigator_contact_information = request.form.get('contact_information')
        investigator_expertise = request.form.get('expertise')
        investigator_case_number = request.form.get('case_number')

        # Save the form data to the database and assign to the case
        sherlock.create_investigator(investigator_badge_number, investigator_name, investigator_contact_information, investigator_expertise)
        sherlock.assigned_to(investigator_case_number, investigator_badge_number)

        # Redirect to a success page or the case details page
        return redirect('/home/{}'.format(investigator_case_number))
    else:
        return render_template('create_investigator.html')
    
@app.route('/create/evidence')
def create_evidence():
    if request.method == 'POST':
        evidence_number = request.form.get('evidence_number')
        evidence_description = request.form.get('description')
        evidence_type = request.form.get('type')
        evidence_timestamp = request.form.get('timestamp')
        evidence_case_number = request.form.get('case_number')

        # Save the form data to the database and assign to the case
        sherlock.create_evidence(evidence_number, evidence_description, evidence_type, evidence_timestamp)
        sherlock.related_to(evidence_case_number, evidence_number)

        # Redirect to a success page or the case details page
        return redirect('/home/{}'.format(evidence_case_number))
    else:
        return render_template('create_evidence.html')

@app.route('/view/suspect')
def view_suspect(suspect_alias):
    # CREATE GET QUERIES
    #sherlock.get
    pass

@app.route('/delete/suspect/<suspect_alias>')
def delete_suspect(suspect_alias):
    # CREATE GET QUERIES
    #sherlock.get
    pass

@app.route('/delete/victim/<victim_name>')
def delete_victim(victim_name):
    # CREATE GET QUERIES
    #sherlock.get
    pass

@app.route('/delete/investigator/<badge_number>')
def delete_investigator(badge_number):
    # CREATE GET QUERIES
    #sherlock.get
    pass

@app.route('/delete/evidence/<evidence_number>')
def delete_evidence(evidence_number):
    # CREATE GET QUERIES
    #sherlock.get
    pass