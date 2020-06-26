# FSND-Capstone
Udacity Full stack Nanodegree capstone project

## Motivation
This project is the Capstone project for Udacity Full Stack Developer Nanodegree. I choose to use my own topic as content for this project. 

Background for this project: I'm developing a Web app to prodict next day's stock behavior for a given company. It will use machine learning and Natural Language Processing to predict stock using previous stock trending and news data. The data are gathered from [my previous project in Data Engineering Nanodegree] (https://github.com/xintao0202/Data-Engineering-Nanodegree/tree/master/Capstone%20Project%20Folder). Also some specific user role can add News to help gather more company specific and up-to-date news data. 

However, for this project, I will not develope the maching learning and prediction part. I will focus on the Web GUI, which will have the following funcitons:

1. The Web app models a company's stock market related information and manage news that could impact stock market. It will let users contribute to the web to help the system make more accurate predictions.  
2. "Regular Users" can view company's information and all the news; "News Writers" can create/modify/delete news on top of the privileges of "Regular Users"; "System Managers" can create/modify/delete companies on top the privileges of "News Writers"

## Project dependencies, local development and hosting instructions
1. Make sure `cd` to the project root folder 
2. Install Python 3, Flask and postgres on your machine if not already
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
3. To test locally, need create a db in postgres database
```
export FLASK_APP=api.py;
flask run --reload
```
API EndPoints tests:

GET '/news'
- fetches a list of news
- Request Arguments: None
- Returns: An object with news objects and success flag
- Curl Request and Server Response example: 
```
curl http://127.0.0.1:5000/news
```

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
curl http://127.0.0.1:5000/news -X POST -H "Content-Type: application/json" -d '{ "title": "Intel new chip", "body": "Intel announced new generation of CPU", "date_time": "2020-05-30 15:30" }'
```
```
{"created":2,"success":true}
```
PATCH '/news/int:id'
- Update a news by id 
- Request Arguments: news_id
- Returns:  A object with three keys- 'success', 'updated' shows the id of the news updated, and the content of the updated news
- Curl Request and Server Response example: 
```
curl http://127.0.0.1:5000/news/2 -X PATCH -H "Content-Type: application/json" -d '{ "title": "AMD new chip", "body": "AMD announced new generation of CPU", "date_time": "2020-06-30 15:30" }'
````

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
curl http://127.0.0.1:5000/news/2 -X DELETE
```
```
{"deleted":"2","success":true}
```

GET '/companies'
- fetches a list of companies
- Request Arguments: None
- Returns: An object with news objects and success flag
- Curl Request and Server Response example: 
```
curl http://127.0.0.1:5000/companies
```

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
curl http://127.0.0.1:5000/companies -X POST -H "Content-Type: application/json" -d '{ "name": "Intel", "address": "Santa Clara, CA", "sector": "semiconductor", "industry": "manufacture" }'
```
```
{"created":2,"success":true}
```
PATCH '/companies/int:id'
- Update a company by id 
- Request Arguments: company_id
- Returns:  A object with three keys- 'success', 'edited' shows the id of the company updated, and the content of the updated company
- Curl Request and Server Response example: 
```
curl http://127.0.0.1:5000/companies/2 -X PATCH -H "Content-Type: application/json" -d '{ "name": "AMD", "address": "One AMD Place P.O. Box 3453 Sunnyvale, CA 94088", "sector": "semiconductor", "industry": "manufacture" }'
```

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
curl http://127.0.0.1:5000/companies/2 -X DELETE
```
```
{"deleted":"2","success":true}
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

Obtain access token:

First access the login page by type the following in broswer

```
https://<domain name>/authorize?audience=<identifier>&response_type=token&client_id=<client id>&redirect_uri=<call back page>
```
Then assgin the roles to the signed up users

Last re-submit the login page, which will direct to the URL with token