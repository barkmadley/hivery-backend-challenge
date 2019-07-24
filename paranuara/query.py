from typing import List, NamedTuple

from paranuara.db import ParanuaraDB
from paranuara.person import Person

JoinPeopleResponse = NamedTuple(
    "JoinPeopleResponse",
    [("person1", Person), ("person2", Person), ("friends_in_common", List[Person])],
)


class ParanuaraQuery:
    def __init__(self, db: ParanuaraDB) -> None:
        self.db = db

    def query_company_employees(self, company_id: int) -> List[Person]:
        company = self.db.fetch_company_by_id(company_id)
        return self.db.fetch_people_by_company_id(company.id)

    def query_join_friends(
        self, person1_id: int, person2_id: int
    ) -> JoinPeopleResponse:
        person1 = self.db.fetch_person_by_id(person1_id)
        person2 = self.db.fetch_person_by_id(person2_id)
        friends_of_person1 = self.db.fetch_friends_of_person(person1)
        friends_of_person2 = self.db.fetch_friends_of_person(person2)
        friends_of_person2_ids = set(person.id for person in friends_of_person2)

        friends_in_common = [
            friend
            for friend in friends_of_person1
            if friend.id in friends_of_person2_ids
            and friend.eye_color == "brown"
            and not friend.has_died
        ]

        return JoinPeopleResponse(
            person1=person1, person2=person2, friends_in_common=friends_in_common
        )

    def query_person(self, person_id: int) -> Person:
        return self.db.fetch_person_by_id(person_id)
