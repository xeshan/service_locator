# Service provider locator

The following rapo aim to develop REST API by which maintain and retrieve service providers.  Deployed on AWS lambda which can access by following API url

https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev

### Stack

Used the follow tech stack:

* [Python]  [Django] [Django Rest Framework] [MySQL] [Redis]


### Installation

Requires Python3.9 or above to run.
```
1. $ virtualenv -p python3 venv      # Create virtualenv
2. $ source venv/bin/activate        # Activate virtualenv
3. $ pip install -r requirements.txt # Install python modules

update database settings

$ python manage.py migrate
```

### Run Server
```
$ python manage.py runserver 
```
### API endpoints

| Methods  | URLs | Params
| ------------- | ------------- | ------------- |
| GET  | api/provider/  | none
| POST  | api/provider/  | name, email, language, currency, phone_number
| PUT  | api/provider/<provider_id>/  | name, email, language, currency, phone_number
| DEL  | api/provider/<provider_id>/  | none
| GET  | api/service-area/  | none
| POST  | api/service-area/  | name, price, poly, provider_id
| PUT  | api/service-area/<service_id>/  | name, price, poly, provider_id
| DEL  | api/service-area/<service_id>/  | none
| PUT  | api/search/  | latitude, longitude 
