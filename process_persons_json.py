import json
import os
from argparse import ArgumentParser

from flanker.addresslib import address

from paranuara.person import person_from_json
from cli_util import add_people_arg


def main():
    parser = ArgumentParser(description="Process people.json files")
    add_people_arg(parser)
    args = parser.parse_args()
    people = json.load(args.people)
    foods = set()
    email_domains = set()
    email_usernames = set()
    for person_dict in people:
        person = person_from_json(person_dict)
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
