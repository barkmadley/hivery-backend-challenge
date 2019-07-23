from typing import List

from paranuara.company import Company
from paranuara.db import CompanyNotFound, ParanuaraDB, PersonNotFound
from paranuara.person import Person


class InMemoryDB(ParanuaraDB):
    def __init__(self, companies: List[Company], people: List[Person]) -> None:
        self.companies = companies
        self.people = people

    def fetch_company_by_id(self, company_id: int) -> Company:
        try:
            return self.companies[company_id]
        except IndexError:
            raise CompanyNotFound

    def fetch_people_by_company_id(self, company_id: int) -> List[Person]:
        return [person for person in self.people if person.company_id == company_id]

    def fetch_person_by_id(self, person_id: int) -> Person:
        try:
            return self.people[person_id]
        except IndexError:
            raise PersonNotFound

    def fetch_friends_of_person(self, person: Person) -> List[Person]:
        return [self.people[person_id] for person_id in person.friends]
