import json
import os
from argparse import ArgumentParser

from paranuara.company import from_json
from cli_util import add_companies_arg


def main():
    parser = ArgumentParser(description="Process companies.json files")
    add_companies_arg(parser)
    args = parser.parse_args()
    companies = json.load(args.companies)
    for company_dict in companies:
        company = from_json(company_dict)
        print(company)


if __name__ == "__main__":
    main()
