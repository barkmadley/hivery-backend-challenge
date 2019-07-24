from typing import Any, Dict, NamedTuple

Company = NamedTuple("Company", [("id", int), ("name", str)])


def company_from_json(dict):
    """
        Example company json:
        {
            "index": 0, ==> id
            "company": "NETBOOK" ==> name
        }
    """
    return Company(id=dict["index"], name=dict["company"])


def json_from_company(company: Company) -> Dict[str, Any]:
    return {
        "index": company.id,
        "company": company.name,
    }
