from typing import Callable, List

from paranuara.company import Company
from paranuara.person import Person


class ParanuaraDB:
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
