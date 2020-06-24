import os
from sqlalchemy import Column, String, Integer, create_engine, Date, Float, DataTime
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

#----------------------------------------------------------------------------#
# Database setup
#----------------------------------------------------------------------------#

database_path = 'postgresql://postgres:123456@localhost:5432/company_news'

db = SQLAlchemy()

'''
setup_db(app)
binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
To create a clean database with no data 
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Dump initialize test data to the database.
'''

def db_init_test_data():
    new_news = (News(
        title = 'AstraZeneca triplet therapy tops doublets in large-scale COPD study',
        body = 'AstraZeneca (AZN -3.8%) announces positive results from a Phase 3 clinical trial, ETHOS, evaluating Breztri Aerosphere (budesonide/glycopyrronium/formoterol fumarate) in patients with moderate-to-severe chronic obstructive pulmonary disease (COPD). The data were presented virtually at the American Thoracic Society Scientific Symposium, Clinical Trials in Pulmonary Medicine and published in the New England Journal of Medicine.',
        date_time = datetime.datetime.now()
        ))

    new_company = (Company(
        name = 'Amazon',
        address = '410 Terry Avenue North, Seattle, WA, 98109-5210, United States'
        sector = 'Consumer Cyclical'
        industy = 'Internet Retail'
        ))

    # predict 0 means do nothing, 1 means buy, -1 means sell
    new_predict = Predict.insert().values(
        company_id = new_company.id,
        news_id = new_news.id,
        stock_predict = 0
    )

    new_news.insert()
    new_company.insert()
    db.session.execute(new_predict) 
    db.session.commit()



#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#

class News(db.Model):  
  __tablename__ = 'news'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  body = Column(String)
  date_time = Column(DataTime)

  def __init__(self, name, gender, age):
    self.title = title
    self.body = body
    self.date_time = date_time

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'body': self.body,
      'date_time': self.date_time
    }


class Company(db.Model):  
  __tablename__ = 'company'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  address = Column(String)
  sector = Column(String)
  industry = Column(String)

  def __init__(self, title, release_date) :
    self.name = name
    self.address = address
    self.sector = sector
    self.industry = industry

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name' : self.name,
      'address': self.address,
      'sector': self.sector,
      'industry': self.industry
    }


# complete relationship models, company and news are N:N relationship
# i.e. some news involves multipe companies
class Predict(db.Model):  
  __tablename__ = 'predict'

  id = Column(Integer, primary_key=True)
  company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=False)
  news_id=db.Column(db.Integer, db.ForeignKey('News.id'), nullable=False)
  company=db.relationship('Company', backref='predict', cascade='all, delete', lazy=True)
  news=db.relationship('News', backref='predict', cascade='all, delete', lazy=True)

