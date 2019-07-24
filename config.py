class BaseConfig:
    COMPANIES_FILE = "resources/companies.json"
    PEOPLE_FILE = "resources/people.json"
    DB = "inmemory"

class DevConfig(BaseConfig):
    DEVELOPMENT = True
    DB = "mongo"
    MONGO_URI = "mongodb://localhost:27017/paranuara"

