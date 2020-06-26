
'''
Tests for jwt flask app.
'''
import os
import json
import unittest

from app import *
from models import *


regular_user_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTdkYTI3Y2JjODUwMDE5MmExZGExIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMxNjIzMjEsImV4cCI6MTU5MzI0ODcyMSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6Y29tcGFuaWVzIiwicmVhZDpuZXdzIl19.cjusPBoTHIzla47PbhETpN2F62PXsNAIirTUgC34ZG_CDYuBq5v8hlPvQmCYo5g31ImvMFWMwGxKr8dJJcoLfl5H7CxjnTsMdG4oMItjjvAqlygLOvkgW8iL_O25UWyhPXE5ffpPYvdP814UiUB0NzqAOXpr6y2Y7PUi9JQ5-NGYLyFdzI-ZOS_DqYMw0t_NTZubtdlmaIPaQo83qoNQkj8ObG1dRlWm3PI_QogSQ8zOVTnW1ZvNgCCdLW8eb6HPEBg5rEFegCHVR7LDc8oJ9Wh_-qbQ5NiMRfbnnTzL1fTXAQEtUJ8mL3WDO2ptiQoFNWUy9Lh1WJKg7OxwjeYHpA"
news_writer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgwMmEyOTk1MzYwMDE0NmEzY2Q5IiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMxNjIzOTksImV4cCI6MTU5MzI0ODc5OSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpuZXdzIiwiZGVsZXRlOm5ld3MiLCJlZGl0Om5ld3MiLCJyZWFkOmNvbXBhbmllcyIsInJlYWQ6bmV3cyJdfQ.i-uu9xBXJ3bkxhaeBveo0rUJ1Ke602J8V-QZ07sUZ1eNyOmkI3_4xbdL63DZ4T9gI60GMmfIbI0_VF4RvESNrYY1MgSSvoWCOv0eo9V8WOr0KtHOSSQKLYrb0N9E3V0raSizaL8MiSg-h1HWfEbObw0k2EAGOR8YzIHG0iXvXjUibdH_SOMOTABZAlrEjerJacLJbB-ykOoLVpf-DNZ6BcZCUZBOST8qUelv7uhsqgp2bWIkj9jpMnCnW0sX0biZTnS__DsCZvcCQLqWOFG323mPA01XKvvSBrV9hkaqNG81IXw1ylQ0uaf3McQTkweM8oBXG04B-EAjrhMgv_aCIw"
system_manager_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgyM2MyOTk1MzYwMDE0NmEzY2VhIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMxNjI1NTAsImV4cCI6MTU5MzI0ODk1MCwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6bmV3cyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6bmV3cyIsImVkaXQ6Y29tcGFuaWVzIiwiZWRpdDpuZXdzIiwicmVhZDpjb21wYW5pZXMiLCJyZWFkOm5ld3MiXX0.lPaGtsAakJhQeHJxSeVwC54KLUhXs3oOtXMQ7SVn2d9LI-A0P6QXliZ3MvPZdddSEBYnu1SGCznpZ5Iiw6_SGxmsaITn-hl2jumq5-olYOoi-syxTJvwTmjIN5mPqgD3JnpyGel8ir5BW0rLgV5k5OwHK-7IedHWOgV2NtJCN-t0x_vYYrU-5ouOuy_CAwoTFKY_LML3AZzFgAeekuXMmwo31KhDO-rnOlIAl3s0gI7NDPtMN_c5zMX_vrVLIcAnJBpvZcYGsC0pWqk861zijdol9QcW3bW-d0ptr3JbmCdPi4UMNCvMKELEUiYYvXTShDtAzA-eGRYXXSDTu7CPAA"

# Create authorization headers using auth key and bearer token

auth_header_regular_user={
    'Authorization': regular_user_token
}

auth_header_news_writer={
    'Authorization': news_writer_token
}

auth_header_system_manager={
    'Authorization': system_manager_token
}

class StockTestCase(unittest.TestCase):
    """This class represents the stock_predict app test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        # uncomment this if you want to start a new database on app refresh
        db_drop_and_create_all() 
        # uncomment this if you want to use test data
        db_init_test_data()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation and for expected errors.
    Good practice for test driven development (TDD)
    """

    # Test all users can view news and company information
    def test_get_news_for_regular_user(self):
        res = self.client().get('/news', headers = auth_header_regular_user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['news'], list)
        self.assertEqual(data['success'], True)

    def test_get_news_for_news_writer(self):
        res = self.client().get('/news', headers = auth_header_news_writer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['news'], list)
        self.assertEqual(data['success'], True)

    def test_get_news_for_system_manager(self):
        res = self.client().get('/news', headers = auth_header_system_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['news'], list)
        self.assertEqual(data['success'], True)

    def test_get_companies_for_regular_user(self):
        res = self.client().get('/companies', headers = auth_header_regular_user)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['companies'], list)
        self.assertEqual(data['success'], True)
    
    def test_get_companies_for_news_writer(self):
        res = self.client().get('/companies', headers = auth_header_news_writer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['companies'], list)
        self.assertEqual(data['success'], True)

    def test_get_companies_for_system_manager(self):
        res = self.client().get('/companies', headers = auth_header_system_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['companies'], list)
        self.assertEqual(data['success'], True)

    # Test get data without authorization
    def test_get_companies_without_auth(self):
        res = self.client().get('/companies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Authorization header is missing.')

    def test_get_news_without_auth(self):
        res = self.client().get('/news')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Authorization header is missing.')

    # Test authorized users can create news 
    def test_create_news_news_writer(self):
        new_news={
            'title': 'Intel new chip',
            'body': 'Intel announced new generation of CPU',
            'date_time': '2020-05-30 15:30'
        }
        res=self.client().post('/news', json=new_news, headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_create_news_system_manager(self):
        new_news={
            'title': 'Tesla new car',
            'body': 'Tesla announced new model car',
            'date_time': '2020-05-26 13:30'
        }
        res=self.client().post('/news', json=new_news, headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    # Test authorized users can create companies 
    def test_create_company_system_manager(self):
        new_company={
            'name': 'Intel',
            'address': 'Santa Clara, CA',
            'sector': 'semiconductor',
            'industry': 'manufacture'
        }
        res=self.client().post('/companies', json=new_company, headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)

     # Test unauthorized users cannot create news 
    def test_create_news_regular_user(self):
        new_news={
            'title': 'Intel new chip',
            'body': 'Intel announced new generation of CPU',
            'date_time': '2020-05-30 15:30'
        }
        res=self.client().post('/news', json=new_news, headers = auth_header_regular_user)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])
    
    def test_create_news_without_header(self):
        new_news={
            'title': 'Intel new chip',
            'body': 'Intel announced new generation of CPU',
            'date_time': '2020-05-30 15:30'
        }
        res=self.client().post('/news', json=new_news)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])
        
    # Test unauthorized users cannot create companies 
    def test_create_company_system_manager(self):
        new_company={
            'name': 'Intel',
            'address': 'Santa Clara, CA',
            'sector': 'semiconductor',
            'industry': 'manufacture'
        }
        res=self.client().post('/companies', json=new_company, headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])

    def test_create_company_without_header(self):
        new_company={
            'name': 'Intel',
            'address': 'Santa Clara, CA',
            'sector': 'semiconductor',
            'industry': 'manufacture'
        }
        res=self.client().post('/companies', json=new_company)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,401)
        self.assertFalse(data['success'])

    # Test for authorized user can update news
    def test_update_news_news_writer(self):
        update_news={
            'date_time': '2020-06-30 14:30'
        }
        res=self.client().patch('/news/1', json=update_news, headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)
    
    def test_update_news_system_manager(self):
        update_news={
            'date_time': '2020-06-29 14:30'
        }
        res=self.client().patch('/news/1', json=update_news, headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 1)

    # Test for authorized user can update company
    def test_update_company_system_manager(self):
        update_news={
            'industry': 'food'
        }
        res=self.client().patch('/companies/1', json=update_news, headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['edited'], 1)

    # Test for unauthorized user cannot update news
    def test_update_news_regular_user(self):
        update_news={
            'date_time': '2020-06-30 14:30'
        }
        res=self.client().patch('/news/1', json=update_news, headers = auth_header_regular_user)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_news_without_header(self):
        update_news={
            'date_time': '2020-06-30 14:30'
        }
        res=self.client().patch('/news/1', json=update_news)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)       

    # Test for unauthorized user cannot update company
    def test_update_company_news_writer(self):
        update_news={
            'industry': 'food'
        }
        res=self.client().patch('/companies/1', json=update_news, headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_company_regular_user(self):
        update_news={
            'industry': 'food'
        }
        res=self.client().patch('/companies/1', json=update_news, headers = auth_header_regular_user)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_company_without_header(self):
        update_news={
            'industry': 'food'
        }
        res=self.client().patch('/companies/1', json=update_news)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Test for invalid id when updating news
    def test_update_news_invalid_id(self):
        update_news={
            'date_time': '2020-06-24 14:30'
        }
        res=self.client().patch('/news/999', json=update_news, headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test for invalid id when updating company
    def test_update_company_invalid_id(self):
        update_company={
            'sector': 'finace'
        }
        res=self.client().patch('/companies/999', json=update_company, headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


     # Test for authorized user can delete news
    def test_delete_news_news_writer(self):
        res=self.client().delete('/news/1', headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
    
    def test_delete_news_system_manager(self):
        res=self.client().delete('/news/1', headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    # Test for authorized user can delete company
    def test_delete_company_system_manager(self):

        res=self.client().delete('/companies/1', headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    # Test for unauthorized user cannot delete news
    def test_delete_news_regular_user(self):
        res=self.client().delete('/news/1', headers = auth_header_regular_user)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_news_without_header(self):
        res=self.client().delete('/news/1')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)       

    # Test for unauthorized user cannot delete company
    def test_delete_company_news_writer(self):
        res=self.client().delete('/companies/1', headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_company_regular_user(self):
        res=self.client().delete('/companies/1', headers = auth_header_regular_user)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_company_without_header(self):
        res=self.client().delete('/companies/1')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Test for invalid id when deleting news
    def test_update_news_invalid_id(self):
        res=self.client().delete('/news/999', headers = auth_header_news_writer)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test for invalid id when updating company
    def test_delete_company_invalid_id(self):
        res=self.client().delete('/companies/999', headers = auth_header_system_manager)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
   







# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()