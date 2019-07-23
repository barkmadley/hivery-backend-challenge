import json
import os
from argparse import ArgumentParser

from flanker.addresslib import address

from paranuara.person import from_json
from util import open_file


def main():
    parser = ArgumentParser(description="Process people.json files")
    parser.add_argument(
        "people", metavar="file", type=open_file, help="people.json filename"
    )
    args = parser.parse_args()
    people = json.load(args.people)
    foods = set()
    email_domains = set()
    email_usernames = set()
    for person_dict in people:
        person = from_json(person_dict)
        foods |= set(person.favourite_food)
        email_parsed = address.parse(person.email)
        if email_parsed:
            email_usernames |= set([email_parsed.mailbox])
            email_domains |= set([email_parsed.hostname])
    print(foods)
    print(email_domains)
    print(len(email_usernames))


if __name__ == "__main__":
    main()
