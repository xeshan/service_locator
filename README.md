# Service provider locator

The following rapo aim to develop REST API by which maintain and retrieve service providers.  Deployed on AWS lambda which can access by following API url

https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev

### Stack

Used the follow tech stack:

* [Python]  [Django] [Django Rest Framework] [Mysql] [AWS Redis]

Live site running AWS RDS for Mysql and AWS Redis for search

### Installation

Requires Python3.9 or above to run.
```
1. $ virtualenv -p python3 venv      # Create virtualenv
2. $ source venv/bin/activate        # Activate virtualenv
3. $ pip install -r requirements.txt # Install python modules
Edit database settings in service_locator/settings.py
$ python manage.py migrate
```

### Run Server
```
$ python manage.py runserver 
```

### Run Fixture for dummy data
```
$ python manage.py loaddata provider
$ python manage.py loaddata servicearea
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
| PUT  | api/search/  | latitude, longitude, point


### API endpoints curl commands

#### Create provider

```
curl --location --request POST 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/provider/' \
--form 'name="zeeshan"' \
--form 'email="zee@zee.com"' \
--form 'language="eng"' \
--form 'currency="USD"' \
--form 'phone_number="999999"'

```
#### GET providers list
```
curl --location --request GET 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/provider/'
```

#### Update provider

```
curl --location --request PUT 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/provider/96a95428-5f59-4291-b8a6-9a36a73ec7a5/' \
--form 'name="zeee"' \
--form 'email="zee@zee.com"' \
--form 'language="eng"' \
--form 'currency="USD"' \
--form 'phone_number="999999"'
```

#### Delete provider
```
curl --location --request DELETE 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/provider/<provider_id>/'

retrieve already created provider id 
e.g.
curl --location --request DELETE 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/provider/96a95428-5f59-4291-b8a6-9a36a73ec7a5/'
```


#### Create service area

```

curl --location --request POST 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/service-area/' \
--form 'name="service area2"' \
--form 'price="99"' \
--form 'poly="{\"type\": \"Feature\",\"properties\": {},\"geometry\": {\"type\": \"Polygon\",\"coordinates\": [[[54.02929688787, 95.9985354183632762], [54.268041998821, 94.83998827780665], [54.77246523998, 95.87674775085432], [54.48745228515676, 95.424946709803654], [54.988762929687985, 94.553599887363009]]]}"' \
--form 'provider_id="<provider_id>"'

p.s retrieve and replace provider_id
```

#### Search service area

```
curl --location --request PUT 'https://b1myqf8gt7.execute-api.us-east-1.amazonaws.com/dev/api/search/' \
--form 'latitude="45.99808905"' \
--form 'longitude="94.895418736387"' 
```
