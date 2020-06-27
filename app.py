import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import *
from flask_migrate import Migrate
import datetime
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  migrate = Migrate(app, db)
  # uncomment this if you want to start a new database on app refresh
  # db_drop_and_create_all() 
  # uncomment this if you want to use test data
  # db_init_test_data()

  # add access control headers
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  

 #----------------------------------------------------------------------------#
 # Filters
 #----------------------------------------------------------------------------#

  def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format="EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)

  app.jinja_env.filters['datetime'] = format_datetime

  
  # Welcome page

  @app.route('/', methods=['POST', 'GET'])
  def home_page():
    """
    Returns list of actors in json format
    """
    return jsonify("Welcome to stock_predict API")
  
  #----------------------------------------------------------------------------#
  # Controllers for "news".
  #----------------------------------------------------------------------------#

  @app.route('/news', methods=['GET'])
  @requires_auth('read:news')
  def read_news(payload):
    """
    Returns list of actors in json format
    """
    news = News.query.all()

    if len(news) == 0:
      abort(404, {'message': 'no news found.'})

    return jsonify({
      'success': True,
      'news': [new.format() for new in news]
    })

  @app.route('/news', methods=['POST'])
  @requires_auth('create:news')
  def create_news(payload):
    """
    add a news
    """
    news = request.get_json()
    if not news:
      abort(400, {'message': 'request not valid.'})
    title = news.get('title', None)
    body = news.get('body', None)
    date_time= news.get('date_time', None)

    if not title or not body or not date_time:
      abort(400, {'message': 'make sure all field is completed.'})

    new_news = (News(
          title = title, 
          body = body,
          date_time = date_time
          ))
    new_news.insert()

    return jsonify({
      'success': True,
      'created': new_news.id
    })

  @app.route('/news/<news_id>', methods=['PATCH'])
  @requires_auth('edit:news')
  def edit_news(payload, news_id):
    """Edit a news
    """
    news = request.get_json()
    if not news_id:
      abort(400, {'message': 'invalid news id'})
    if not news:
      abort(400, {'message': 'request not valid'})

    news_edit = News.query.filter(News.id == news_id).one_or_none()
    if not news_edit:
      abort(404, {'message': 'News not found.'})

    title = news.get('title', news_edit.title)
    body = news.get('body', news_edit.body)
    date_time= news.get('date_time', news_edit.date_time)

    news_edit.title = title
    news_edit.body = body
    news_edit.date_time = date_time
    news_edit.update()

    return jsonify({
      'success': True,
      'updated': news_edit.id,
      'news' : [news_edit.format()]
    })

  @app.route('/news/<news_id>', methods=['DELETE'])
  @requires_auth('delete:news')
  def delete_news(payload, news_id):
    """
    Delete a news
    """
    if not news_id:
      abort(400, {'message': 'invalid news id.'})
    news = News.query.filter(News.id == news_id).one_or_none()
    if not news:
        abort(404, {'message': 'News not found.'})
    
    news.delete()

    return jsonify({
      'success': True,
      'deleted': news.id
    })

  #----------------------------------------------------------------------------#
  # Controllers for "company".
  #----------------------------------------------------------------------------#

  @app.route('/companies', methods=['GET'])
  @requires_auth('read:companies')
  def read_companies(payload):
    """ 
    return list of companies in JSON format
    """
    companies = Company.query.all()

    if len(companies) == 0:
      abort(404, {'message': 'Companies not found.'})

    return jsonify({
      'success': True,
      'companies': [company.format() for company in companies]
    })

  @app.route('/companies', methods=['POST'])
  @requires_auth('create:companies')
  def create_company(payload):
    """
    Create a company
    """
    company = request.get_json()
    if not company:
          abort(400, {'message': 'invalid request.'})

    name = company.get('name', None)
    address = company.get('address', None)
    sector = company.get('sector', None)
    industry = company.get('industry', None)

    if not name or not address or not sector or not industry:
      abort(422, {'message': 'missing inputs.'})

    new_comapny = (Company(
      name = name,
      address = address,
      sector = sector,
      industry = industry
          ))
    new_comapny.insert()

    return jsonify({
      'success': True,
      'created': new_comapny.id
    })

  @app.route('/companies/<company_id>', methods=['PATCH'])
  @requires_auth('edit:companies')
  def edit_companies(payload, company_id):
    """
    Edit a company
  
    """
    company = request.get_json()
    if not company_id:
      abort(400, {'message': 'invalid company id.'})
    if not company:
      abort(400, {'message': 'invalid request'})
    company_edit = Company.query.filter(Company.id == company_id).one_or_none()

    if not company_edit:
      abort(404, {'message': 'company not found'})

    name = company.get('name', company_edit.name)
    address = company.get('address', company_edit.address)
    sector = company.get('sector', company_edit.sector)
    industry = company.get('industry', company_edit.industry)

    company_edit.name = name
    company_edit.address = address
    company_edit.sector = sector
    company_edit.industry = industry

    company_edit.update()

    return jsonify({
      'success': True,
      'edited': company_edit.id,
      'company' : [company_edit.format()]
    })

  @app.route('/companies/<company_id>', methods=['DELETE'])
  @requires_auth('delete:companies')
  def delete_companies(payload, company_id):
    """
    Delete a company
    """
    
    if not company_id:
      abort(400, {'message': 'invalid company id.'})

    company_delete = Company.query.filter(Company.id == company_id).one_or_none()

    if not company_delete:
        abort(404, {'message': 'company not found'})
    
    company_delete.delete()
    
    return jsonify({
      'success': True,
      'deleted': company_delete.id
    })

  #----------------------------------------------------------------------------#
  # Error Handlers
  #----------------------------------------------------------------------------#

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
              "success": False,
              "error": 422,
              }), 422

  @app.errorhandler(400)
  def unprocessable(error):
      return jsonify({
              "success": False,
              "error": 400,
              }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
      }), 404

  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify({
          "success": False,
          "error": error.status_code,
          "message": error.error['description']
      }), error.status_code

  return app

#----------------------------------------------------------------------------#
# Run App
#----------------------------------------------------------------------------#


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)