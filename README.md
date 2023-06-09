# Sherlock

<img src="/app/static/SHERLOCK.png"  width="150" height="150">


## About
**A Web Application for Crime Scene Investigation - CSI**

Elements you can include and deal with: 
1. Case: Represents a criminal case.
Properties: case number, description, date created, status, etc.

2. Suspect: Represents a person suspected of involvement in a crime.
Properties: name, aliases, date of birth, physical description, etc.

3. Victim: Represents a person who has been harmed or affected by a crime.
Properties: name, age, contact information, etc.

4. Investigator: Represents an investigator or a team of investigators assigned to a case.
Properties: name, badge number, expertise, contact information, etc.

5. Evidence: Represents a piece of evidence related to a case.
Properties: type (e.g., document, photo, video), description, timestamp, etc.

## Languages & Technologies
- Python
- Flask
- Neo4j
- Cypher
- HTML & CSS

## How to Run it
1. pip3 install -r requirements.txt
2. source venv/bin/activate
3. cd app
4. flask --app app run
> Remember to create your Neo4j before and change the DB credentials with yours in app.py, line 8.
