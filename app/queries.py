from flask import jsonify

class Query:
    def __init__(self, database):
        self.db = database

    # -----------------------------------------CREATE--------------------------------------------------
    # (:Case {caseNumber: "C001",description: "Robbery at Main Street",status: "Open"})
    def create_case(self, caseNumber: str, description: str, status: str):
        query = "CREATE (:Case {caseNumber: $caseNumber, description: $description, status: $status})"
        parameters = {"caseNumber": caseNumber, "description": description, "status": status}
        self.db.execute_query(query, parameters)

    # (:Suspect {name: "John Doe", alias: "Big Joe", dateOfBirth: "1985-01-15", physicalDescription: "Tall"})
    def create_suspect(self, name: str, alias: str, dateOfBirth: str, physicalDescription: str):
        query = "CREATE (:Suspect {name: $name, alias: $alias, dateOfBirth: $dateOfBirth, physicalDescription: $physicalDescription})"
        parameters = {"name": name, "alias": alias, "dateOfBirth": dateOfBirth, "physicalDescription": physicalDescription}
        self.db.execute_query(query, parameters)

    # (:Victim {contactInformation: "robert@example.com",name: "Robert Johnson",age: 42})
    def create_victim(self, id: str, name: str, age: int, contactInformation: str):
        query = "CREATE (:Victim {name: $name, age: $age, contactInformation: $contactInformation})"
        parameters = {"name": name, "age": age, "contactInformation": contactInformation}
        self.db.execute_query(query, parameters)

    # (:Investigator {contactInformation: "smith@example.com",name: "Detective Smith",badgeNumber: "D001",expertise: "Forensics"})
    def create_investigator(self, badgeNumber: str, name: str, contactInformation: str, expertise: str):
        query = "CREATE (:Investigator {name: $name, badgeNumber: $badgeNumber, contactInformation: $contactInformation, expertise: $expertise})"
        parameters = {"name": name, "badgeNumber": badgeNumber, "contactInformation": contactInformation, "expertise": expertise}
        self.db.execute_query(query, parameters)

    # (:Evidence {description: "Surveillance footage", type: "Document", timestamp: "2023-05-15 10:30:00"})
    def create_evidence(self, evidenceNumber: int, description: str, type: str, timestamp: str):
        query = "CREATE (:Evidence {evidenceNumber: $evidenceNumber, description: $description, type: $type, timestamp: $timestamp})"
        parameters = {"evidenceNumber": evidenceNumber, "description": description, "type": type, "timestamp": timestamp}
        self.db.execute_query(query, parameters)


    # -----------------------------------------CREATE RELATIONSHIPS----------------------------------------
    # Associate Investigator to Cases
    def assigned_to(self, caseNumber: str, badgeNumber: str):
        query = "MATCH (i:Investigator {badgeNumber: $badgeNumber}) MATCH (c:Case {caseNumber: $caseNumber}) CREATE (i)-[:ASSIGNED_TO]->(c)"
        parameters = {"badgeNumber": badgeNumber, "caseNumber": caseNumber}
        self.db.execute_query(query, parameters)
    # Associate Suspect to Cases
    def involved_in(self, caseNumber, suspectName):
        query = "MATCH (s:Suspect {name: $name}) MATCH (c:Case {caseNumber: $caseNumber}) CREATE (s)-[:INVOLVED_IN]->(c)"
        parameters = {"name": suspectName, "caseNumber": caseNumber}
        self.db.execute_query(query, parameters)

    # Associate Victim to Cases
    def affected(self, caseNumber, victimName):
        query = "MATCH (v:Victim {name: $name}) MATCH (c:Case {caseNumber: $caseNumber}) CREATE (v)-[:AFFECTED]->(c)"
        parameters = {"name": victimName, "caseNumber": caseNumber}
        self.db.execute_query(query, parameters)

    # Associate Evidence to Cases
    def related_to(self, caseNumber, evidenceNumber):
        query = "MATCH (e:Evidence {evidenceNumber: $evidenceNumber}) MATCH (c:Case {caseNumber: $caseNumber}) CREATE (e)-[:RELATED_TO]->(c)"
        parameters = {"evidenceNumber": evidenceNumber, "caseNumber": caseNumber}
        self.db.execute_query(query, parameters)


    # -----------------------------------------GET--------------------------------------------------
    # Get all the caseNumbers to navigate through the Cases and display Case details after
    def get_cases_all(self):
        query = "MATCH (c:Case) RETURN c.caseNumber as caseNumber"
        results = self.db.execute_query(query)
        return [result["caseNumber"] for result in results]

    # Returns all about that case: investigators, suspects, victim and evidences
    def get_case(self, caseNumber):
        query = """
            MATCH (c:Case {caseNumber: $caseNumber})
            OPTIONAL MATCH (c)<-[:INVOLVED_IN]-(suspect:Suspect)
            OPTIONAL MATCH (c)<-[:AFFECTED]-(victim:Victim)
            OPTIONAL MATCH (c)<-[:ASSIGNED_TO]-(investigator:Investigator)
            OPTIONAL MATCH (c)<-[:RELATED_TO]-(evidence:Evidence)
            RETURN c, COLLECT(DISTINCT suspect) AS suspects, COLLECT(DISTINCT victim) AS victims,
                COLLECT(DISTINCT investigator) AS investigators, COLLECT(DISTINCT evidence) AS evidences
        """
        parameters = {"caseNumber": caseNumber}
        data = self.db.execute_query(query, parameters)
        if data:
            # Cleanning data
            data = data[0]

            # dict of node case
            case = dict(data[0])

            suspects = dict(data[1])
            print(suspects)
            victims = data[2]
            investigators = data[3]
            evidences = data[4]

            # Extracting the properties of the case node
            case_properties = case.properties
            case_number = case_properties['caseNumber']

            # Extracting the properties of the suspects
            suspects_data = []
            for suspect in suspects:
                suspect_properties = suspect.properties
                suspect_data = {
                    'name': suspect_properties['name'],
                    'aliases': suspect_properties['aliases'],
                    'date_of_birth': suspect_properties['dateOfBirth'],
                    'physical_description': suspect_properties['physicalDescription']
                }
                suspects_data.append(suspect_data)

            # Extracting the properties of the victims
            victims_data = []
            for victim in victims:
                victim_properties = victim.properties
                victim_data = {
                    'name': victim_properties['name'],
                    'age': victim_properties['age'],
                    'contact_information': victim_properties['contactInformation']
                }
                victims_data.append(victim_data)

            # Extracting the properties of the investigators
            investigators_data = []
            for investigator in investigators:
                investigator_properties = investigator.properties
                investigator_data = {
                    'name': investigator_properties['name'],
                    'badge_number': investigator_properties['badgeNumber'],
                    'contact_information': investigator_properties['contactInformation'],
                    'expertise': investigator_properties['expertise']
                }
                investigators_data.append(investigator_data)

            # Extracting the properties of the evidences
            evidences_data = []
            for evidence in evidences:
                evidence_properties = evidence.properties
                evidence_data = {
                    'description': evidence_properties['description'],
                    'type': evidence_properties['type'],
                    'timestamp': evidence_properties['timestamp']
                }
                evidences_data.append(evidence_data)

            response = {
                'case': case_number,
                'suspects': suspects_data,
                'victims': victims_data,
                'investigators': investigators_data,
                'evidences': evidences_data
            }
            print("response: " + response)
            return jsonify(response)
        else:
            return jsonify({'error': 'Case not found'}), 404

    # -----------------------------------------UPDATE--------------------------------------------------
    # Modify Case status
    def update_case(self, caseNumber, status):
        query = "MATCH (c:Case {caseNumber: $caseNumber}) SET c.status = $status"
        parameters = {"caseNumber": caseNumber, "status": status}
        self.db.execute_query(query, parameters)


    # -----------------------------------------DELETE--------------------------------------------------
    def delete_case(self, caseNumber):
        query = "MATCH (c:Case {caseNumber: $caseNumber}) DETACH DELETE c"
        parameters = {"caseNumber": caseNumber}
        self.db.execute_query(query, parameters)
    
    def delete_investigator(self, badgeNumber):
        query = "MATCH (i:Investigator {badgeNumber: $badgeNumber}) DETACH DELETE i"
        parameters = {"badgeNumber": badgeNumber}
        self.db.execute_query(query, parameters)

    def delete_evidence(self, evidenceNumber):
        query = "MATCH (e:Evidence {evidenceNumber: $evidenceNumber}) DETACH DELETE e"
        parameters = {"evidenceNumber": evidenceNumber}
        self.db.execute_query(query, parameters)

    def delete_suspect(self, name):
        query = "MATCH (s:Suspect {name: $name}) DETACH DELETE s"
        parameters = {"name": name}
        self.db.execute_query(query, parameters)