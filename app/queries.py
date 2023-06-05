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
    def create_victim(self, victim_id: str, name: str, age: int, contactInformation: str):
        query = "CREATE (:Victim {victim_id: $victim_id, name: $name, age: $age, contactInformation: $contactInformation})"
        parameters = {"victim_id": victim_id, "name": name, "age": age, "contactInformation": contactInformation}
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
            # Cleanning data (All the data is at the first position)
            data = data[0]

            # Dict of node case
            case = dict(data[0])

            # List of lists containing everything
            suspects = data[1]
            suspects_list = []
            for suspect in suspects:
                suspect_dict = {}
                # Extracting properties from the node and inserting in a dict
                suspect_dict["name"] = suspect['name']
                suspect_dict["alias"] = suspect['alias']
                suspect_dict["dateOfBirth"] = suspect['dateOfBirth']
                suspect_dict["physicalDescription"] = suspect['physicalDescription']

                suspects_list.append(suspect_dict)

            victims = data[2]
            victims_list = []
            for victim in victims:
                victim_dict = {}
                victim_dict["id"] = victim["id"]
                victim_dict["name"] = victim["name"]
                victim_dict["age"] = victim["age"]
                victim_dict["contactInformation"] = victim["contactInformation"]
                
                victims_list.append(victim_dict)

            investigators = data[3]
            investigators_list = []
            for investigator in investigators:
                investigator_dict = {}
                investigator_dict["badgeNumber"] = investigator["badgeNumber"]
                investigator_dict["name"] = investigator["name"]
                investigator_dict["contactInformation"] = investigator["contactInformation"]
                investigator_dict["expertise"] = investigator["expertise"]

                investigators_list.append(investigator_dict)

            evidences = data[4]
            evidences_list = []
            for evidence in evidences:
                evidences_dict = {}
                evidences_dict["evidenceNumber"] = evidence["evidenceNumber"]
                evidences_dict["description"] = evidence["description"]
                evidences_dict["type"] = evidence["type"]
                evidences_dict["timestamp"] = evidence["timestamp"]

                evidences_list.append(evidences_dict)
            
            # Packing everything to send
            response = []
            response.append(case)
            response.append(suspects_list)
            response.append(victims_list)
            response.append(investigators_list)
            response.append(evidences_list)

            return response
        else:
            return jsonify({'error': 'Case not found'}), 404
        

    def get_suspect(self, suspect_alias):
        query = "MATCH (s:Suspect {alias: $suspect_alias}) return s"
        parameters = {"suspect_alias": suspect_alias}
        return self.db.execute_query(query, parameters)
    
    def get_victim(self, victim_id):
        query = "MATCH (v:Victim {victim_id: $victim_id}) return v"
        parameters = {"victim_id": victim_id}
        return self.db.execute_query(query, parameters)
    
    def get_investigator(self, badgeNumber):
        query = "MATCH (i:Investigator {badgeNumber: $badgeNumber}) return i"
        parameters = {"badgeNumber": badgeNumber}
        return self.db.execute_query(query, parameters)
    
    def get_evidence(self, evidenceNumber):
        query = "MATCH (e:Evidence {evidenceNumber: $evidenceNumber}) return e"
        parameters = {"evidenceNumber": evidenceNumber}
        response = self.db.execute_query(query, parameters)
        return response

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

    def delete_victim(self, id):
        query = "MATCH (v:Victim {victim_id: $victim_id}) DETACH DELETE v"
        parameters = {"victim_id": id}
        self.db.execute_query(query, parameters)