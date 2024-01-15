# fastapi_template

> This is a FastAPI template. 
> If you identify anything that requires optimization, kindly submit a pull request (PR) or open an issue. 
> The example app is provided for reference purposes only, feel free to remove it once you start using the template.

## How to config?
You can configure various environment settings in the `configs.py` file.

## How to develop?

### 1. add tests
Following TDD, add tests in the `unittests` directory to validate the expected outcomes.

### 2. add api routes
1. Add the models in `models.__init__.py`.
2. Add the schemas for validating API data in `example.schemas`
3. Add API routes in `example.api`
4. Add exceptions in `example.exceptions`
5. Add common business logic in `example.services`

# How to start?

Start dependencies:
```
cd docker
docker-compose up -d
```

Run server:
```
cd src
poetry install
python manage.py migrate
python manage.py start
```
