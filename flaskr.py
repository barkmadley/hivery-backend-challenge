import json
import os
from typing import Any, Dict, List

from flanker.addresslib import address
from flask import Flask, abort, jsonify

from in_memory_db import InMemoryDB
from paranuara.company import from_json as company_from_json
from paranuara.db import CompanyNotFound, PersonNotFound
from paranuara.person import from_json as person_from_json
from paranuara.query import ParanuaraQuery


def person_to_json(person):
    email = address.parse(person.email)
    username = None
    if email:
        username = email.mailbox
    return {
        "username": username,
        "age": str(person.age),
        "fruits": person.fruits,
        "vegetables": person.vegetables,
    }


def init_app(companies_file: str, people_file: str) -> ParanuaraQuery:
    companies_json = json.load(open(companies_file))
    companies = [company_from_json(company_dict) for company_dict in companies_json]

    people_json = json.load(open(people_file))
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
        try:
            people = query.query_company_employees(company_id)
            json = [person_to_json(person) for person in people]
            return jsonify(json)
        except CompanyNotFound:
            return abort(404)

    @app.route("/person/<int:person_id>")
    def person(person_id):
        try:
            result = query.query_person(person_id)
            return jsonify(person_to_json(result))
        except PersonNotFound:
            return abort(404)

    @app.route("/person/<int:person1_id>/friends_join/<int:person2_id>")
    def friends_join(person1_id, person2_id):
        result = query.query_join_friends(person1_id, person2_id)
        return jsonify(result._asdict())

    return app
