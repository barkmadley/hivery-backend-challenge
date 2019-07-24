from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from paranuara.company import Company
from paranuara.db import CompanyNotFound, ParanuaraDB, PersonNotFound
from paranuara.person import Person
from paranuara.query import JoinPeopleResponse, ParanuaraQuery


def generate_person(id=None, eye_color="red", has_died=False, friends=[]):
    return Person(
        id=id,
        mongo_id="mongo_id",
        guid="guid",
        has_died=has_died,
        balance=Decimal(),
        picture="picture",
        age=10,
        eye_color=eye_color,
        name="name",
        gender="gender",
        company_id=None,
        email="email",
        phone="phone",
        address="address",
        about="about",
        registered=datetime.now(),
        tags=["tags"],
        friends=friends,
        greeting="greeting",
        favourite_food=["favouriteFoods"],
    )


class ParanuaraQueryTest_query_company_employees(TestCase):
    def test_has_employees(self):
        person1 = generate_person(id=1)
        company = Company(id=0, name="test")
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=lambda id: company,
                fetch_people_by_company_id=lambda id: [person1],
                fetch_people_by_ids=None,
                fetch_person_by_id=None,
            )
        )

        result = query.query_company_employees(company_id=0)

        self.assertEqual(result, [person1])

    def test_no_employees(self):
        company = Company(id=0, name="test")
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=lambda id: company,
                fetch_people_by_company_id=lambda id: [],
                fetch_people_by_ids=None,
                fetch_person_by_id=None,
            )
        )

        result = query.query_company_employees(company_id=0)

        self.assertEqual(result, [])

    def test_no_company(self):
        def fetch_company_by_id(id):
            raise CompanyNotFound()

        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=fetch_company_by_id,
                fetch_people_by_company_id=lambda id: [],
                fetch_people_by_ids=None,
                fetch_person_by_id=None,
            )
        )

        with self.assertRaises(CompanyNotFound):
            query.query_company_employees(company_id=0)


class ParanuaraQueryTest_query_person(TestCase):
    def test_not_found(self):
        def fetch_person_by_id(id):
            raise PersonNotFound()

        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=None,
                fetch_person_by_id=fetch_person_by_id,
            )
        )

        with self.assertRaises(PersonNotFound):
            query.query_person(person_id=0)

    def test_found(self):
        person = generate_person(0)
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=None,
                fetch_person_by_id=lambda id: person,
            )
        )

        result = query.query_person(person_id=0)

        self.assertEqual(result, person)


class ParanuaraQueryTest_query_join_friends(TestCase):
    def test_person1_not_found(self):
        def fetch_person_by_id(id):
            if id == 1:
                raise PersonNotFound()
            else:
                return generate_person(2)

        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=None,
                fetch_person_by_id=fetch_person_by_id,
            )
        )

        with self.assertRaises(PersonNotFound):
            query.query_join_friends(person1_id=1, person2_id=2)

    def test_person2_not_found(self):
        def fetch_person_by_id(id):
            if id == 2:
                raise PersonNotFound()
            return generate_person(1)

        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=None,
                fetch_person_by_id=fetch_person_by_id,
            )
        )
        with self.assertRaises(PersonNotFound):
            query.query_join_friends(person1_id=1, person2_id=2)

    def test_no_friends(self):
        person1 = generate_person(1)
        person2 = generate_person(2)
        people = {1: person1, 2: person2}
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=lambda ids: [people.get(id) for id in ids],
                fetch_person_by_id=lambda id: people.get(id),
            )
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )

    def test_1_friend_in_common(self):
        person1 = generate_person(1, friends=[3])
        person2 = generate_person(2, friends=[3])
        friend_in_common = generate_person(3, eye_color="brown", has_died=False)
        people = {1: person1, 2: person2, 3: friend_in_common}
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=lambda ids: [people.get(id) for id in ids],
                fetch_person_by_id=lambda id: people.get(id),
            )
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(
                person1=person1, person2=person2, friends_in_common=[friend_in_common]
            ),
        )

    def test_intersection(self):
        person1 = generate_person(1, friends=[3, 4])
        person2 = generate_person(2, friends=[3, 5])
        friend_in_common = generate_person(3, eye_color="brown", has_died=False)
        friend_of_person1 = generate_person(4, eye_color="brown", has_died=False)
        friend_of_person2 = generate_person(5, eye_color="brown", has_died=False)
        people = {
            1: person1,
            2: person2,
            3: friend_in_common,
            4: friend_of_person1,
            5: friend_of_person2,
        }
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=lambda ids: [people.get(id) for id in ids],
                fetch_person_by_id=lambda id: people.get(id),
            )
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(
                person1=person1, person2=person2, friends_in_common=[friend_in_common]
            ),
        )

    def test_eye_color_filter(self):
        person1 = generate_person(1, friends=[3])
        person2 = generate_person(2, friends=[3])
        friend_in_common = generate_person(3, eye_color="black", has_died=False)
        people = {1: person1, 2: person2, 3: friend_in_common}
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=lambda ids: [people.get(id) for id in ids],
                fetch_person_by_id=lambda id: people.get(id),
            )
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )

    def test_has_died_filter(self):
        person1 = generate_person(1, friends=[3])
        person2 = generate_person(2, friends=[3])
        friend_in_common = generate_person(3, eye_color="brown", has_died=True)
        people = {1: person1, 2: person2, 3: friend_in_common}
        query = ParanuaraQuery(
            db=ParanuaraDB(
                fetch_company_by_id=None,
                fetch_people_by_company_id=None,
                fetch_people_by_ids=lambda ids: [people.get(id) for id in ids],
                fetch_person_by_id=lambda id: people.get(id),
            )
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )
