import os

def open_file(path):
    path = os.path.realpath(path)
    return open(path)

def add_companies_arg(parser):
    parser.add_argument(
        "--companies", metavar="file", type=open_file, help="companies.json filename"
    )

def add_people_arg(parser):
    parser.add_argument(
        "--people", metavar="file", type=open_file, help="people.json filename"
    )
