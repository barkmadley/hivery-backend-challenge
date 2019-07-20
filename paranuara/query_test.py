from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from paranuara.company import Company
from paranuara.person import Person
from paranuara.query import ParanauraQuery, JoinPeopleResponse


class CompanyNotFound(Exception):
    pass


class PersonNotFound(Exception):
    pass


def genPerson(id=None, eye_color="red", has_died=False):
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
        friends=[id + 1],
        greeting="greeting",
        favourite_food=["favouriteFoods"],
        fruits=[],
        vegetables=[],
    )


class ParanauraQueryTest_query_company_employees(TestCase):
    def test_has_employees(self):
        person1 = genPerson(id=1)
        company = Company(id=0, name="test")
        query = ParanauraQuery(
            fetch_company_by_id=lambda id: company,
            fetch_people_by_company_id=lambda id: [person1],
            fetch_friends_of_person=None,
            fetch_person_by_id=None,
        )

        result = query.query_company_employees(company_id=0)

        self.assertEqual(result, [person1])

    def test_no_employees(self):
        company = Company(id=0, name="test")
        query = ParanauraQuery(
            fetch_company_by_id=lambda id: company,
            fetch_people_by_company_id=lambda id: [],
            fetch_friends_of_person=None,
            fetch_person_by_id=None,
        )

        result = query.query_company_employees(company_id=0)

        self.assertEqual(result, [])

    def test_no_company(self):
        def fetch_company_by_id(id):
            raise CompanyNotFound()

        query = ParanauraQuery(
            fetch_company_by_id=fetch_company_by_id,
            fetch_people_by_company_id=lambda id: [],
            fetch_friends_of_person=None,
            fetch_person_by_id=None,
        )

        with self.assertRaises(CompanyNotFound):
            query.query_company_employees(company_id=0)


class ParanauraQueryTest_query_person(TestCase):
    def test_not_found(self):
        def fetch_person_by_id(id):
            raise PersonNotFound()

        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=None,
            fetch_person_by_id=fetch_person_by_id,
        )

        with self.assertRaises(PersonNotFound):
            query.query_person(person_id=0)

    def test_found(self):
        person = genPerson(0)
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=None,
            fetch_person_by_id=lambda id: person,
        )

        result = query.query_person(person_id=0)

        self.assertEqual(result, person)


class ParanauraQueryTest_query_join_friends(TestCase):
    def test_person1_not_found(self):
        def fetch_person_by_id(id):
            if id == 1:
                raise PersonNotFound()
            else:
                return genPerson(2)

        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=None,
            fetch_person_by_id=fetch_person_by_id,
        )

        with self.assertRaises(PersonNotFound):
            query.query_join_friends(person1_id=1, person2_id=2)

    def test_person2_not_found(self):
        def fetch_person_by_id(id):
            if id == 2:
                raise PersonNotFound()
            return genPerson(1)

        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=None,
            fetch_person_by_id=fetch_person_by_id,
        )

        with self.assertRaises(PersonNotFound):
            query.query_join_friends(person1_id=1, person2_id=2)

    def test_no_friends(self):
        person1 = genPerson(1)
        person2 = genPerson(2)
        people = {1: person1, 2: person2}
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=lambda person: [],
            fetch_person_by_id=lambda id: people.get(id),
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )

    def test_1_friend_in_common(self):
        person1 = genPerson(1)
        person2 = genPerson(2)
        friend_in_common = genPerson(3, eye_color="brown", has_died=False)
        people = {1: person1, 2: person2}
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=lambda person: [friend_in_common],
            fetch_person_by_id=lambda id: people.get(id),
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(
                person1=person1, person2=person2, friends_in_common=[friend_in_common]
            ),
        )

    def test_intersection(self):
        person1 = genPerson(1)
        person2 = genPerson(2)
        friend_in_common = genPerson(3, eye_color="brown", has_died=False)
        friend_of_person1 = genPerson(4, eye_color="brown", has_died=False)
        friend_of_person2 = genPerson(5, eye_color="brown", has_died=False)
        people = {1: person1, 2: person2}
        friends_of = {
            1: [friend_in_common, friend_of_person1],
            2: [friend_in_common, friend_of_person2],
        }
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=lambda person: friends_of.get(person.id),
            fetch_person_by_id=lambda id: people.get(id),
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(
                person1=person1, person2=person2, friends_in_common=[friend_in_common]
            ),
        )

    def test_eye_color_filter(self):
        person1 = genPerson(1)
        person2 = genPerson(2)
        friend_in_common = genPerson(3, eye_color="black", has_died=False)
        people = {1: person1, 2: person2}
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=lambda person: [friend_in_common],
            fetch_person_by_id=lambda id: people.get(id),
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )

    def test_has_died_filter(self):
        person1 = genPerson(1)
        person2 = genPerson(2)
        friend_in_common = genPerson(3, eye_color="brown", has_died=True)
        people = {1: person1, 2: person2}
        query = ParanauraQuery(
            fetch_company_by_id=None,
            fetch_people_by_company_id=None,
            fetch_friends_of_person=lambda person: [friend_in_common],
            fetch_person_by_id=lambda id: people.get(id),
        )

        result = query.query_join_friends(person1_id=1, person2_id=2)

        self.assertEqual(
            result,
            JoinPeopleResponse(person1=person1, person2=person2, friends_in_common=[]),
        )
