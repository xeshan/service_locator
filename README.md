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