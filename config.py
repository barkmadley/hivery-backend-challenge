class BaseConfig:
    COMPANIES_FILE = "resources/companies.json"
    PEOPLE_FILE = "resources/people.json"

class DevConfig(BaseConfig):
    DEVELOPMENT = True
