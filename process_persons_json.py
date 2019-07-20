from argparse import ArgumentParser

import os
import json

from paranuara.person import from_json

def open_file(path):
    path = os.path.realpath(path)
    return open(path)


def main():
    parser = ArgumentParser(description="Process people.json files")
    parser.add_argument(
        "people", metavar="file", type=open_file, help="people.json filename"
    )
    args = parser.parse_args()
    people = json.load(args.people)
    foods = set()
    for person_dict in people:
        person = from_json(person_dict)
        foods |= set(person.favourite_food)
    print(foods)


if __name__ == "__main__":
    main()
