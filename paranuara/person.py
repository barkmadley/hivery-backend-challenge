from datetime import datetime
from decimal import Decimal
from typing import List, NamedTuple, Optional

Person = NamedTuple(
    "Person",
    [
        ("id", int),
        ("mongo_id", str),
        ("guid", str),
        ("has_died", bool),
        ("balance", Decimal),
        ("picture", str),
        ("age", int),
        ("eye_color", str),
        ("name", str),
        ("gender", str),
        ("company_id", Optional[int]),
        ("email", str),
        ("phone", str),
        ("address", str),
        ("about", str),
        ("registered", datetime),
        ("tags", List[str]),
        ("friends", List[int]),
        ("greeting", str),
        ("favourite_food", List[str]),
        ("fruits", List[str]),
        ("vegetables", List[str]),
    ],
)


def datetime_from_json(str: str) -> datetime:
    return datetime.fromisoformat(str)


def decimal_from_json(str: str) -> Decimal:
    return Decimal(str.replace("$", "").replace(",", ""))


def friend_index_from_json(dict) -> int:
    return dict["index"]


def friends_list_from_json(array) -> List[int]:
    return [friend_index_from_json(dict) for dict in array]


# All foods seen in the given people.json
ALL_FOODS = {
    "banana",
    "orange",
    "celery",
    "strawberry",
    "cucumber",
    "beetroot",
    "apple",
    "carrot",
}

# All known vegetables + lettuce which was in the README.md file
VEGETABLES = {"celery", "beetroot", "cucumber", "carrot", "lettuce"}

FRUITS = {"banana", "orange", "strawberry", "apple"}


def vegetables_from_foods(foods):
    return [food for food in foods if food in VEGETABLES]


def fruits_from_foods(foods):
    return [food for food in foods if food in FRUITS]


def from_json(dict):
    """
        Example person json:
        {
            "_id": "595eeb9b96d80a5bc7afb106",
            "index": 0,
            "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
            "has_died": true,
            "balance": "$2,418.59",
            "picture": "http://placehold.it/32x32",
            "age": 61,
            "eyeColor": "blue",
            "name": "Carmella Lambert",
            "gender": "female",
            "company_id": 58,
            "email": "carmellalambert@earthmark.com",
            "phone": "+1 (910) 567-3630",
            "address": "628 Sumner Place, Sperryville, American Samoa, 9819",
            "about": "...",
            "registered": "2016-07-13T12:29:07 -10:00",
            "tags": [
                "id",
                "quis",
                "ullamco",
                "consequat",
                "laborum",
                "sint",
                "velit"
            ],
            "friends": [
                {
                    "index": 0
                },
                {
                    "index": 1
                },
                {
                    "index": 2
                }
            ],
            "greeting": "Hello, Carmella Lambert! You have 6 unread messages.",
            "favouriteFood": [
                "orange",
                "apple",
                "banana",
                "strawberry"
            ]
        }
    """
    return Person(
        id=dict["index"],
        mongo_id=dict["_id"],
        guid=dict["guid"],
        has_died=dict["has_died"],
        balance=decimal_from_json(dict["balance"]),
        picture=dict["picture"],
        age=dict["age"],
        eye_color=dict["eyeColor"],
        name=dict["name"],
        gender=dict["gender"],
        company_id=dict.get("company_id"),
        email=dict["email"],
        phone=dict["phone"],
        address=dict["address"],
        about=dict["about"],
        registered=datetime_from_json(dict["registered"]),
        tags=dict["tags"],
        friends=friends_list_from_json(dict["friends"]),
        greeting=dict["greeting"],
        favourite_food=dict["favouriteFood"],
        fruits=fruits_from_foods(dict["favouriteFood"]),
        vegetables=vegetables_from_foods(dict["favouriteFood"]),
    )
