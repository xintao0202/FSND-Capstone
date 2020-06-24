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