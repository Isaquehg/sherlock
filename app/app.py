# flask --app app run
from flask import Flask, redirect, render_template, request
from database import Database
from queries import Query

app = Flask(__name__)
db = Database("bolt://44.203.85.235:7687", "neo4j", "sky-privilege-confusions")
sherlock = Query(db)

# -------------------------------------------HOME-------------------------------------------------------

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

# -------------------------------------------CREATE-------------------------------------------------------

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
        victim_id = request.form.get('victim_id')
        victim_name = request.form.get('victim_name')
        victim_age = request.form.get('age')
        victim_contact_information = request.form.get('contact_information')
        victim_case_number = request.form.get('case_number')

        # Save the form data to the database and assign to the case
        sherlock.create_victim(victim_id, victim_name, victim_age, victim_contact_information)
        sherlock.affected(victim_case_number, victim_id)

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

# -------------------------------------------GET-------------------------------------------------------

@app.route('/view/suspect/<suspect_alias>')
def view_suspect(suspect_alias):
    suspect = sherlock.get_suspect(suspect_alias)
    suspect = dict(suspect[0])
    suspect = suspect['s']

    suspect_dict = {}
    for property in suspect:
        suspect_dict["name"] = suspect["name"]
        suspect_dict["alias"] = suspect["alias"]
        suspect_dict["dateOfBirth"] = suspect["dateOfBirth"]

    return render_template('view_suspect.html', suspect=suspect_dict)

@app.route('/view/victim/<victim_id>')
def view_victim(victim_id):
    victim = sherlock.get_victim(victim_id)

    victim = dict(victim[0])
    victim = victim['v']

    victim_dict = {}
    for property in victim:
        victim_dict["victim_id"] = victim["victim_id"]
        victim_dict["name"] = victim["name"]
        victim_dict["age"] = victim["age"]
        victim_dict["contactInformation"] = victim["contactInformation"]

    return render_template('view_victim.html', victim=victim_dict)

@app.route('/view/investigator/<badge_number>')
def view_investigator(badge_number):
    investigator = sherlock.get_investigator(badge_number)

    investigator = dict(investigator[0])
    investigator = investigator['i']

    investigator_dict = {}
    for property in investigator:
        investigator_dict["badgeNumber"] = investigator["badgeNumber"]
        investigator_dict["name"] = investigator["name"]
        investigator_dict["contactInformation"] = investigator["contactInformation"]
        investigator_dict["expertise"] = investigator["expertise"]

    return render_template('view_investigator.html', investigator=investigator_dict)

@app.route('/view/evidence/<evidence_number>')
def view_evidence(evidence_number):
    evidence = sherlock.get_evidence(evidence_number)

    evidence = dict(evidence[0])
    evidence = evidence['e']

    evidence_dict = {}
    for property in evidence:
        evidence_dict["evidenceNumber"] = evidence["evidenceNumber"]
        evidence_dict["description"] = evidence["description"]
        evidence_dict["type"] = evidence["type"]
        evidence_dict["timestamp"] = evidence["timestamp"]

    print(evidence_dict)

    return render_template('view_evidence.html', evidence=evidence_dict)

# -------------------------------------------DELETE-------------------------------------------------------

@app.route('/delete/suspect/<suspect_alias>')
def delete_suspect(suspect_alias):
    sherlock.delete_suspect(suspect_alias)

    # Redirect to a success page or the case details page
    return redirect('/home')

@app.route('/delete/victim/<victim_id>')
def delete_victim(victim_id):
    sherlock.delete_victim(victim_id)

    return redirect('/home')

@app.route('/delete/investigator/<badge_number>')
def delete_investigator(badge_number):
    sherlock.delete_investigator(badge_number)

    return redirect('/home')

@app.route('/delete/evidence/<evidence_number>')
def delete_evidence(evidence_number):
    sherlock.delete_evidence(evidence_number)

    return redirect('/home')