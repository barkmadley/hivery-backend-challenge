import json
import os
from argparse import ArgumentParser

from paranuara.company import from_json
from util import open_file


def main():
    parser = ArgumentParser(description="Process companies.json files")
    parser.add_argument(
        "companies", metavar="file", type=open_file, help="companies.json filename"
    )
    args = parser.parse_args()
    companies = json.load(args.companies)
    for company_dict in companies:
        company = from_json(company_dict)
        print(company)


if __name__ == "__main__":
    main()
