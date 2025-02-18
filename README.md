# Setup Instructions:

### 0. First time setup

This python application depends on python3.

```
$ make setup
Please run 'source .venv/bin/activate' to enter virtualenv for subsequent commands
```

### Install python dependencies

```
(.venv) $ make dep
...
Successfully intalled appdirs-1.4.3 ... werkzeug-0.15.5
```

### Testing

```
(.venv) $ make typecheck lint test
```

### Running the server

```
(.venv) $ make run
```

# Configuration options

## Configuring the location of the companies/people JSON files

Modify the lines in `config.py` that set the constants `COMPANIES_FILE` and `PEOPLE_FILE`

## Configuring the database

Modify the lines in `config.py` that set `DB` and `MONGO_URI`.

Setting `DB` to `"mongo"` will load the json blobs into the mongo specified by
`MONGO_URI` and then serve the requests from that DB.

Only a little bit of time has been spent optmising the mongo backend.

Setting `DB` to `"inmemory"` will load the json blobs into memory and just do
index based lookups

# Manual Testing

```
$ curl http://localhost:5000/company/1/employees | jq length
7
```

```
$ curl http://localhost:5000/person/1
{
  "age": "60",
  "fruits": [],
  "username": "deckermckenzie",
  "vegetables": [
    "cucumber",
    "beetroot",
    "carrot",
    "celery"
  ]
}
```

```
$ curl http://localhost:5000/person/1/friends_join/10
{
  "friends_in_common": [
    {
      ...
      "email": "deckermckenzie@earthmark.com",
      ...
    }
  ]
  "person1": {
    ...
    "email": "deckermckenzie@earthmark.com",
    ...
  }
  "person2": {
    ...
    "email": "kathleenclarke@earthmark.com",
    ...
  }
}
```

```
$ curl http://localhost:5000/company/arbitrary/employees
404
```

```
$ curl http://localhost:5000/company/100000/employees
404
```

```
$ curl http://localhost:5000/person/100000
404
```

```
$ curl http://localhost:5000/person/arbitrary
404
```

```
$ curl http://localhost:5000/person/10000/friends_join/10
404
```

```
$ curl http://localhost:5000/person/1/friends_join/100000
404
```

# Paranuara Challenge

Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features

Your API must provides these end points:

- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Delivery

To deliver your system, you need to send the link on GitHub. Your solution must provide tasks to install dependencies, build the system and run. Solutions that does not fit this criteria **will not be accepted** as a solution. Assume that we have already installed in our environment Java, Ruby, Node.js, Python, MySQL, MongoDB and Redis; any other technologies required must be installed in the install dependencies task. Moreover well tested and designed systems are one of the main criteria of this assessement

## Evaluation criteria

- Solutions written in Python would be preferred.
- Installation instructions that work.
- During installation, we may use different companies.json or people.json files.
- The API must work.
- Tests

Feel free to reach to your point of contact for clarification if you have any questions.
