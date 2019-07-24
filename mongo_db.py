from typing import List

from paranuara.company import Company, company_from_json, json_from_company
from paranuara.db import CompanyNotFound, ParanuaraDB, PersonNotFound
from paranuara.person import Person, json_from_person, person_from_json


class MongoDB(ParanuaraDB):
    def __init__(self, companies: List[Company], people: List[Person], mongo) -> None:
        self.mongo = mongo
        for company in companies:
            company_dict = json_from_company(company)
            self.mongo.db.company.replace_one(
                {"index": company_dict["index"]}, company_dict, upsert=True
            )
        for person in people:
            person_dict = json_from_person(person)
            self.mongo.db.person.replace_one(
                {"_id": person_dict["_id"]}, person_dict, upsert=True
            )
        # TODO: setup index: company.index
        # TODO: setup index: person.index
        # TODO: setup index: person.company_id

    def fetch_company_by_id(self, company_id: int) -> Company:
        results = list(self.mongo.db.company.find({"index": company_id}))
        if len(results) == 0:
            raise CompanyNotFound
        else:
            return company_from_json(results[0])

    def fetch_people_by_company_id(self, company_id: int) -> List[Person]:
        return [
            person_from_json(result)
            for result in self.mongo.db.person.find({"company_id": company_id})
        ]

    def fetch_person_by_id(self, person_id: int) -> Person:
        results = list(self.mongo.db.person.find({"index": person_id}))
        if len(results) == 0:
            raise PersonNotFound
        else:
            return person_from_json(results[0])

    def fetch_friends_of_person(self, person: Person) -> List[Person]:
        # TODO: not efficient
        return [self.fetch_person_by_id(person_id) for person_id in person.friends]
