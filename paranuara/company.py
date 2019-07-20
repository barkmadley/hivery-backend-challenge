from typing import NamedTuple

Company = NamedTuple("Company", [("id", int), ("name", str)])


def from_json(dict):
    """
        Example company json:
        {
            "index": 0, ==> id
            "company": "NETBOOK" ==> name
        }
    """
    return Company(id=dict["index"], name=dict["company"])
