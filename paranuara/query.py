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
        friend_ids_in_common = set(person1.friends) & set(person2.friends)
        friends_in_common_full = self.db.fetch_people_by_ids(list(friend_ids_in_common))

        friends_in_common = [
            friend
            for friend in friends_in_common_full
            if friend.eye_color == "brown"
            and not friend.has_died
        ]

        return JoinPeopleResponse(
            person1=person1, person2=person2, friends_in_common=friends_in_common
        )

    def query_person(self, person_id: int) -> Person:
        return self.db.fetch_person_by_id(person_id)
