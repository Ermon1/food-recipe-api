from django.test import SimpleTestCase

from app import  calk 
class TestValu(SimpleTestCase):
    def testAdd(self):
        res=calk.add(5,5)
        self.assertEqual(res,10)
        
    
    def test_subtract(self):
        res = calk.subtract(10,15)
        
        self.assertEqual(res,5)