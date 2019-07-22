import json
import os

from flask import Flask, jsonify

from paranuara.company import from_json as company_from_json
from paranuara.person import from_json as person_from_json
from paranuara.query import ParanuaraQuery

from in_memory_db import InMemoryDB


def person_to_json(person):
    dict = person._asdict()
    dict["balance"] = str(dict["balance"])
    return dict


def init_app(companies: str, people: str) -> ParanuaraQuery:
    companies_json = json.load(open(companies))
    companies = [company_from_json(company_dict) for company_dict in companies_json]

    people_json = json.load(open(people))
    people = [person_from_json(person_dict) for person_dict in people_json]

    db = InMemoryDB(companies, people)

    return ParanuaraQuery(db=db)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    query = init_app("resources/companies.json", "resources/people.json")

    @app.route("/company/<int:company_id>/employees")
    def company_employees(company_id):
        people = query.query_company_employees(company_id)
        json = [person_to_json(person) for person in people]
        return jsonify(json)

    @app.route("/person/<int:person_id>")
    def person(person_id):
        result = query.query_person(person_id)
        return jsonify(person_to_json(result))

    @app.route("/person/<int:person1_id>/friends_join/<int:person2_id>")
    def friends_join(person1_id, person2_id):
        result = query.query_join_friends(person1_id, person2_id)
        return jsonify(result._asdict())

    return app
