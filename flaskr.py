import json
import os
from typing import Any, Dict, List

from flanker.addresslib import address
from flask import Flask, abort, jsonify
from flask_pymongo import PyMongo

from in_memory_db import InMemoryDB
from mongo_db import MongoDB
from paranuara.company import from_json as company_from_json
from paranuara.db import CompanyNotFound, PersonNotFound
from paranuara.person import (
    Person,
    fruits_from_foods,
    json_from_person,
    person_from_json,
    vegetables_from_foods,
)
from paranuara.query import JoinPeopleResponse, ParanuaraQuery


def json_from_join_people_response(
    join_people_response: JoinPeopleResponse
) -> Dict[str, Any]:
    return {
        "person1": json_from_person(join_people_response.person1),
        "person2": json_from_person(join_people_response.person2),
        "friends_in_common": [
            json_from_person(person)
            for person in join_people_response.friends_in_common
        ],
    }


def person_to_simple_json(person: Person) -> Dict[str, Any]:
    email = address.parse(person.email)
    username = None
    if email:
        username = email.mailbox
    return {
        "username": username,
        "age": str(person.age),
        "fruits": fruits_from_foods(person.favourite_food),
        "vegetables": vegetables_from_foods(person.favourite_food),
    }


class DBNotConfigured(Exception):
    pass


def init_db(companies: List[Company], people: List[Person], app):
    if app.config["DB"] == "inmemory":
        return InMemoryDB(companies, people)
    elif app.config["DB"] == "mongo":
        assert app.config["MONGO_URI"]
        return MongoDB(companies, people, PyMongo(app))
    raise DBNotConfigured()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object("config.DevConfig")
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    companies_json = json.load(open(app.config["COMPANIES_FILE"]))
    companies = [company_from_json(company_dict) for company_dict in companies_json]

    people_json = json.load(open(app.config["PEOPLE_FILE"]))
    people = [person_from_json(person_dict) for person_dict in people_json]

    db = init_db(companies, people, app)
    query = ParanuaraQuery(db=db)

    @app.route("/company/<int:company_id>/employees")
    def company_employees(company_id):
        try:
            people = query.query_company_employees(company_id)
            json = [json_from_person(person) for person in people]
            return jsonify(json)
        except CompanyNotFound:
            return abort(404)

    @app.route("/person/<int:person_id>")
    def person(person_id):
        try:
            result = query.query_person(person_id)
            return jsonify(person_to_simple_json(result))
        except PersonNotFound:
            return abort(404)

    @app.route("/person/<int:person1_id>/friends_join/<int:person2_id>")
    def friends_join(person1_id, person2_id):
        try:
            query_result = query.query_join_friends(person1_id, person2_id)
            return jsonify(json_from_join_people_response(query_result))
        except PersonNotFound:
            raise abort(404)

    return app
