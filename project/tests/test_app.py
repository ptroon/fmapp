# basic app tests


import os
import unittest

from project import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        pass
        app.config['TESTING'] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

#################################################################
# HELPER #
##########
    def login(self, login_id, password):
        return self.app.post(
            '/fpa/login',
            data=dict(login_id=login_id, password=password),
            follow_redirects=True
            )

################################################################
# TESTS #
#########

    def test_main_page(self):
        response = self.app.get('/fpa/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.login('philip', 'test111')
        self.assertEqual(response.status_code, 200)
        print(response.data)

    def test_parameters_page(self):
        response = self.app.get('/admin/parameters', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
