# FSND-Capstone
Udacity Full stack Nanodegree capstone project

## Motivation
This project is the Capstone project for Udacity Full Stack Developer Nanodegree. I choose to use my own topic as content for this project. 

Background for this project: I'm developing a Web app to predict next day's stock behavior for a given company. It will use machine learning and Natural Language Processing to predict stock using previous stock trending and news data. The data are gathered from [my previous project in Data Engineering Nanodegree] (https://github.com/xintao0202/Data-Engineering-Nanodegree/tree/master/Capstone%20Project%20Folder). Also some specific user role can add News to help gather more company specific and up-to-date news data. 

However, for this project, I will not develope the maching learning and prediction part. I will focus on the Web API, which will have the following funcitons:

1. The Web API models a company's stock market related information and manage news that could impact stock market. It will let users contribute to the system in order to more accurate predictions.  
2. "Regular Users" can view company's information and all the news; "News Writers" can create/modify/delete news on top of the privileges of "Regular Users"; "System Managers" can create/modify/delete companies on top the privileges of "News Writers"

## Project dependencies, local development and hosting instructions
1. Make sure `cd` to the project root folder 
2. Install Python 3.5 or higher, Flask and postgres on your machine if not already
3. Initialize and activate a virtualenv:
```
$ cd YOUR_PROJECT_DIRECTORY_PATH/
$ virtualenv --no-site-packages env_capstone
$ source env/Scripts/activate.bat
```
4. Install the depedencies:
```
$ pip install -r requirements.txt
```

## Detailed instructions for scripts

### Run and test scripts locally
1. Build database models in `models.py` using SQLAlchemy
2. Make db connections, build API endpoints and error handlers in `app.py` 
3. Create a db in postgres database, set flask app and run locally
```
export FLASK_APP=api.py;
flask run --reload
```

4. Setup Application/APIs/Roles in Auth0 account, amd complete `auth.py` accordingly. permissions and roles who can access are

Permissions for `regular user`
```
read:news
read:companies
```

Additional permissions for `news writer`
```
create:news
edit:news
delete:news
```

Additional permissions for `system manager`
```
create:companies
edit:companies
delete:companies
``` 

5. Obtain access token:

First access the login page by typing the following in broswer. 

```
https://<domain name>/authorize?audience=<identifier>&response_type=token&client_id=<client id>&redirect_uri=<call back page>
```
Then assgin the roles to the signed up users. Last re-submit the login page, which will direct to the URL with token

5. Completed the unittest `test_app` and tested locally with role/permission tests. All test passed

6. Deploy the API on Heroku 

- Create Heroku account and install Heroku with Homebrew
```
brew tap heroku/brew && brew install heroku
```
- Login to Heroku in Heroku CLI
```
heroku login
```
- Pip install gunicorn and Create `Procfile`. Put the following code in the file
```
gunicorn
```
- create a file `setup.sh`, put the following Config variables in it. 
```
export AUTH0_DOMAIN='dev-eid5kfny.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='stock'
export CLIENT_ID='EUZLOtNKB92XPB408qBffR9VHNxP74Wj'
export DATABASE_URL='postgres://vfirnxrvtpnrrl:ef0033d6fdca7a7e7e1c80e60a724e256bf83e1c658dda002c991d6319ee795d@ec2-18-214-119-135.compute-1.amazonaws.com:5432/d94v2kqjdd3lfs'
```
- Database management and Migrations 
```
pip install flask_script
pip install flask_migrate
pip install psycopg2-binary
```
Create a file `manage.py`
```
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app
from models import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
```
run our local migrations
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
- generate `requirements.txt`
```
pip freeze > requirements.txt
```
- Push to Heroku server
```
heroku create name_of_your_app
git remote add heroku heroku_git_url
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
heroku config --app name_of_your_application # to check config variables
```
- add config vars in Heroku API settings
- run migrations
```
heroku run python manage.py db upgrade --app name_of_your_applicatio
```

- Heroku link: https://stock-predict-app-version0.herokuapp.com/


## API behavior and RBAC controls

URL for localhost test: http://127.0.0.1:5000

URL for Heroku test: https://stock-predict-app-version0.herokuapp.com/

Tokens (expiring in 24 hours)

```
regular_user_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTdkYTI3Y2JjODUwMDE5MmExZGExIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkxMjQsImV4cCI6MTU5MzMwNTUyNCwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6Y29tcGFuaWVzIiwicmVhZDpuZXdzIl19.SuxfsPQxnslfWN0nOsh637muOytZaX96IQGPpQ4nhQMCxtjwDQeYJPI19HBwXlXl3RaDKnCtbi8xVgx3Nko5d6dJ54knjM3P_6aPOg6H83BMZvj22Ftgpe--pIgbrFfUKn-ONZ7lRtJZJKac7SJff3OjHhwU4bMnU7MpCGa6IbQPAi6C0lyG8Hhka3_HK7ualADk2X1CIs0Xv7ukN_5lcpkb3nqEzXVNP2hBU5_0u2vgvg9cT6uF81KR2JIyON7Fns4Vk9wABG-wqieDPlJDCz7dCeHL8KMnZX3pVZoQtduGqoAxfyjNuuCa-mT1xN91iFhM-7sUtFT0XC6bFSZE4Q"

news_writer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgwMmEyOTk1MzYwMDE0NmEzY2Q5IiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkyNjUsImV4cCI6MTU5MzMwNTY2NSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpuZXdzIiwiZGVsZXRlOm5ld3MiLCJlZGl0Om5ld3MiLCJyZWFkOmNvbXBhbmllcyIsInJlYWQ6bmV3cyJdfQ.InjXZNBBRJ22xLRCr_NWA7yMwBfH5sSx0cRzbrzxcdYQCX81kmYqI8mpllxWSar1QvDvgvmi2ZHYISrm88ft-0XOQCpiRxd3HWa2d5wdWGC70L-y1qFbtAuP8nx7TUAPQV85qBcoi_Kf4Y7DXRYj_3OprJ5TMiIesA02RgmC50CT1sHM3W1VcFxdOW_4sHm9sZKGGqEXYZwEiIN8owtbtCyXBeyCmeSORU7h4gWO7pp3RGcmLbTx-ZuCylGqUW6pj-0BTK0tqp8cnPPVf-IwKDh83u4F3mdRagl8Wu4uUac53HZTYGgND5iIL9hUGDd7T0x7E-vu-0NmbtnixR2RpQ"

system_manager_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgyM2MyOTk1MzYwMDE0NmEzY2VhIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkzODEsImV4cCI6MTU5MzMwNTc4MSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6bmV3cyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6bmV3cyIsImVkaXQ6Y29tcGFuaWVzIiwiZWRpdDpuZXdzIiwicmVhZDpjb21wYW5pZXMiLCJyZWFkOm5ld3MiXX0.dJNgevu6g3MZ6KEQ4BcsXMA6RzFUj-MGy5-Y-s_i6wmXiqaXdCk1dUV7wG_vQkWz5tEO6B1PqKZ4vMu8SSn_p-eMXR9Y5lDN_44Kyy3qR-VqtkGMKJHLVNdLuSDSFA8IcD4ss7b7q4KIOkgjsup9OSrmY3Q5Gu4mmStlp17s4TC7oTXewdtTYu7_Eyg-GltXltKslC7s0NV3cIhrxJjtpJcVhR9vfYkAWlJ7TdX3s7VFCMeRtRYbxTXuQDin8Hc8L4nRlt1KxjSu3Tclm71eP-Qh4N0QgiGfi5GiHwoOqpUqJfrDe4iw4_jydwXkvqWvHaauT8fZyPaFc1g9W24wRg"

```

Note the Following Endpoint didn't include Token. I've been used Postman for Endpoint tests and all passed

For 'PATCH' and 'POST', need to add Body content ("raw") for the inputs. There is a 'code' button if we want to convert the request to Curl.

RBAC controls are implmented using the Tokens, which has to be included in the http request. If using token of different roles, it will throw permission error. All the authorization tests are autmated in test_app.py. Of course, it can be tested using Postman or Curl.

GET '/' or POST '/'
- this is welcome page
```
curl <URL>

```
- Response
```
"Welcome to stock_predict API"
```

GET '/news'  
- fetches a list of news
- Request Arguments: None
- Returns: An object with news objects and success flag
- Curl Request and Server Response example: 
```
curl <URL>/news  
```
- Response
```
{"news":
[{"body":"AstraZeneca (AZN -3.8%) announces positive results from a Phase 3 clinical trial, ETHOS, evaluating Breztri Aerosphere (budesonide/glycopyrronium/formoterol fumarate) in patients with moderate-to-severe chronic obstructive pulmonary disease (COPD). The data were presented virtually at the American Thoracic Society Scientific Symposium, Clinical Trials in Pulmonary Medicine and published in the New England Journal of Medicine.","date_time":"Thu, 25 Jun 2020 15:54:09 GMT","id":1,"title":"AstraZeneca triplet therapy tops doublets in large-scale COPD study"}],
"success":true}

```

POST '/news'
- create a news 
- Request Arguments: A json object contains 'title', 'body', 'date_time'
- Returns:  A object with two keys- 'success', and 'created' shows the id of the new news
- Curl Request and Server Response example: 
```
curl <URL>/news -X POST -H "Content-Type: application/json" -d '{ "title": "Intel new chip", "body": "Intel announced new generation of CPU", "date_time": "2020-05-30 15:30" }'
```
- Response
```
{"created":2,"success":true}
```
PATCH '/news/int:id'
- Update a news by id 
- Request Arguments: news_id
- Returns:  A object with three keys- 'success', 'updated' shows the id of the news updated, and the content of the updated news
- Curl Request and Server Response example: 
```
curl <URL>/news/2 -X PATCH -H "Content-Type: application/json" -d '{ "title": "AMD new chip", "body": "AMD announced new generation of CPU", "date_time": "2020-06-30 15:30" }'
````
- Response
```
{"news":[{"body":"AMD announced new generation of CPU",
"date_time":"Tue, 30 Jun 2020 15:30:00 GMT","id":2,"title":"AMD new chip"}],
"success":true,"updated":2}
```

DELETE '/news/int:id'
- Delete a news by id 
- Request Arguments: news_id
- Returns:  A object with two keys- 'success' and 'deleted' shows the id of the news deleted
- Curl Request and Server Response example: 
```
curl <URL>/news/2 -X DELETE
```
- Response
```
{"deleted":"2","success":true}
```

GET '/companies'
- fetches a list of companies
- Request Arguments: None
- Returns: An object with news objects and success flag
- Curl Request and Server Response example: 
```
curl <URL>/companies
```
- Response
```
{"companies":
[{"address":"410 Terry Avenue North, Seattle, WA, 98109-5210, United States","id":1,"industry":"Internet Retail","name":"Amazon","sector":"Consumer Cyclical"}],
"success":true}
```

POST '/companies'
- create a company 
- Request Arguments: A json object contains 'name', 'address', 'sector', 'industry'
- Returns:  A object with two keys- 'success', and 'created' shows the id of the new company
- Curl Request and Server Response example: 
```
curl <URL>/companies -X POST -H "Content-Type: application/json" -d '{ "name": "Intel", "address": "Santa Clara, CA", "sector": "semiconductor", "industry": "manufacture" }'
```
- Response
```
{"created":2,"success":true}
```
PATCH '/companies/int:id'
- Update a company by id 
- Request Arguments: company_id
- Returns:  A object with three keys- 'success', 'edited' shows the id of the company updated, and the content of the updated company
- Curl Request and Server Response example: 
```
curl <URL>/companies/2 -X PATCH -H "Content-Type: application/json" -d '{ "name": "AMD", "address": "One AMD Place P.O. Box 3453 Sunnyvale, CA 94088", "sector": "semiconductor", "industry": "manufacture" }'
```
- Response
```
{"company":[{
"address":"One AMD Place P.O. Box 3453 Sunnyvale, CA 94088",
"id":2,
"industry":"manufacture",
"name":"AMD",
"sector":"semiconductor"}],
"edited":2,
"success":true}

```

DELETE '/companies/int:id'
- Delete a company by id 
- Request Arguments: company_id
- Returns:  A object with two keys- 'success' and 'deleted' shows the id of the company deleted
- Curl Request and Server Response example: 
```
curl <URL>/companies/2 -X DELETE
```
- Response
```
{"deleted":"2","success":true}
```