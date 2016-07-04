from django.test import TestCase
from django.test import Client

# Create your tests here.
class FirstTestCase(TestCase):
    def setUp(self):
        pass 
    
    def test_can_login(self):
        c = Client()
        response = c.post('/login/', {'username': 'john', 'password': 'smith'})
        self.assertEqual(200, response.status_code, "Oh fuck!") 
        print response.content
