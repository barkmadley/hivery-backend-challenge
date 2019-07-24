from typing import Callable, List

from paranuara.company import Company
from paranuara.person import Person


class CompanyNotFound(Exception):
    pass


class PersonNotFound(Exception):
    pass


class ParanuaraDB:
    def __init__(
        self,
        fetch_company_by_id: Callable[[int], Company],
        fetch_people_by_company_id: Callable[[int], List[Person]],
        fetch_person_by_id: Callable[[int], Person],
        fetch_people_by_ids: Callable[[List[int]], List[Person]],
    ) -> None:
        self.fetch_company_by_id = fetch_company_by_id
        self.fetch_people_by_company_id = fetch_people_by_company_id
        self.fetch_person_by_id = fetch_person_by_id
        self.fetch_people_by_ids = fetch_people_by_ids
