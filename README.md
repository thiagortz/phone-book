# Phone Book
Service responsible for recording call details and calculating monthly bills for a particular phone number.

### Environments
| Environment | URL |
|------------|---------|
| production  | https://thephonebook.herokuapp.com


### Docs
| Doc | URL |
|------------|---------|
| Postman Collection  | https://www.getpostman.com/collections/d01cfacaf47bc40be23c
| Doc | https://documenter.getpostman.com/view/1939702/RWaKU9bm#da8c693d-d0d5-4a0e-ba97-3a621ecee8c2

### Work Environment
|  |  |
|------------|---------|
| Operating System | Linux - Ubuntu
| IDE | PyCharm |
|Libraries | requirements.txt |
|DB | PostgreSQL |
### Installation

```
add the same envs sample file: .env.example
```

```sh
pip install -r requirements.txt
```

### Start Application
```shell
python src/main.py
```

### Running Tests

First, you need to install the test runner (nosetests)

```shell
pip install -r requirements-dev.txt
```

To run all tests, use the test runner at the root of the project:
To run all the tests, you can use nosetests from the root of project

```shell
nosetests
```

Also, you can run only unit tests:

```shell
nosetests tests/unit
```

To measure test coverage, run the command bellow

```shell
nosetests --with-coverage --cover-package=src  --cover-inclusive --cover-html
```



