from collections import namedtuple
from typing import Callable, List

from paranuara.company import Company
from paranuara.person import Person

JoinPeopleResponse = namedtuple(
    "JoinPeopleResponse", ["person1", "person2", "friends_in_common"]
)


class ParanauraQuery:
    def __init__(
        self,
        fetch_company_by_id: Callable[[int], Company],
        fetch_people_by_company_id: Callable[[int], List[Person]],
        fetch_person_by_id: Callable[[int], Person],
        fetch_friends_of_person: Callable[[Person], List[Person]],
    ) -> None:
        self.fetch_company_by_id = fetch_company_by_id
        self.fetch_people_by_company_id = fetch_people_by_company_id
        self.fetch_person_by_id = fetch_person_by_id
        self.fetch_friends_of_person = fetch_friends_of_person

    def query_company_employees(self, company_id: int) -> List[Person]:
        company = self.fetch_company_by_id(company_id)
        return self.fetch_people_by_company_id(company.id)

    def query_join_friends(
        self, person1_id: int, person2_id: int
    ) -> JoinPeopleResponse:
        person1 = self.fetch_person_by_id(person1_id)
        person2 = self.fetch_person_by_id(person2_id)
        friends_of_person1 = self.fetch_friends_of_person(person1)
        friends_of_person2 = self.fetch_friends_of_person(person2)
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
        return self.fetch_person_by_id(person_id)
