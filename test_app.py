
'''
Tests for jwt flask app.
'''
import os
import json
import unittest

from app import *
from models import *


regular_user_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTdkYTI3Y2JjODUwMDE5MmExZGExIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkxMjQsImV4cCI6MTU5MzMwNTUyNCwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6Y29tcGFuaWVzIiwicmVhZDpuZXdzIl19.SuxfsPQxnslfWN0nOsh637muOytZaX96IQGPpQ4nhQMCxtjwDQeYJPI19HBwXlXl3RaDKnCtbi8xVgx3Nko5d6dJ54knjM3P_6aPOg6H83BMZvj22Ftgpe--pIgbrFfUKn-ONZ7lRtJZJKac7SJff3OjHhwU4bMnU7MpCGa6IbQPAi6C0lyG8Hhka3_HK7ualADk2X1CIs0Xv7ukN_5lcpkb3nqEzXVNP2hBU5_0u2vgvg9cT6uF81KR2JIyON7Fns4Vk9wABG-wqieDPlJDCz7dCeHL8KMnZX3pVZoQtduGqoAxfyjNuuCa-mT1xN91iFhM-7sUtFT0XC6bFSZE4Q"
news_writer_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgwMmEyOTk1MzYwMDE0NmEzY2Q5IiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkyNjUsImV4cCI6MTU5MzMwNTY2NSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpuZXdzIiwiZGVsZXRlOm5ld3MiLCJlZGl0Om5ld3MiLCJyZWFkOmNvbXBhbmllcyIsInJlYWQ6bmV3cyJdfQ.InjXZNBBRJ22xLRCr_NWA7yMwBfH5sSx0cRzbrzxcdYQCX81kmYqI8mpllxWSar1QvDvgvmi2ZHYISrm88ft-0XOQCpiRxd3HWa2d5wdWGC70L-y1qFbtAuP8nx7TUAPQV85qBcoi_Kf4Y7DXRYj_3OprJ5TMiIesA02RgmC50CT1sHM3W1VcFxdOW_4sHm9sZKGGqEXYZwEiIN8owtbtCyXBeyCmeSORU7h4gWO7pp3RGcmLbTx-ZuCylGqUW6pj-0BTK0tqp8cnPPVf-IwKDh83u4F3mdRagl8Wu4uUac53HZTYGgND5iIL9hUGDd7T0x7E-vu-0NmbtnixR2RpQ"
system_manager_token = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZwT1hXRnNCVmRUVTRvQk45c1p2aiJ9.eyJpc3MiOiJodHRwczovL2Rldi1laWQ1a2ZueS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVmNTgyM2MyOTk1MzYwMDE0NmEzY2VhIiwiYXVkIjoic3RvY2siLCJpYXQiOjE1OTMyMTkzODEsImV4cCI6MTU5MzMwNTc4MSwiYXpwIjoiRVVaTE90TktCOTJYUEI0MDhxQmZmUjlWSE54UDc0V2oiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpjb21wYW5pZXMiLCJjcmVhdGU6bmV3cyIsImRlbGV0ZTpjb21wYW5pZXMiLCJkZWxldGU6bmV3cyIsImVkaXQ6Y29tcGFuaWVzIiwiZWRpdDpuZXdzIiwicmVhZDpjb21wYW5pZXMiLCJyZWFkOm5ld3MiXX0.dJNgevu6g3MZ6KEQ4BcsXMA6RzFUj-MGy5-Y-s_i6wmXiqaXdCk1dUV7wG_vQkWz5tEO6B1PqKZ4vMu8SSn_p-eMXR9Y5lDN_44Kyy3qR-VqtkGMKJHLVNdLuSDSFA8IcD4ss7b7q4KIOkgjsup9OSrmY3Q5Gu4mmStlp17s4TC7oTXewdtTYu7_Eyg-GltXltKslC7s0NV3cIhrxJjtpJcVhR9vfYkAWlJ7TdX3s7VFCMeRtRYbxTXuQDin8Hc8L4nRlt1KxjSu3Tclm71eP-Qh4N0QgiGfi5GiHwoOqpUqJfrDe4iw4_jydwXkvqWvHaauT8fZyPaFc1g9W24wRg"

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
        # db_drop_and_create_all() 
        # uncomment this if you want to use test data
        # db_init_test_data()

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