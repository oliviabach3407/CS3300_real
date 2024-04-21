from django.test import TestCase
from beekeeping_app.models import Apiary, Hive, Keeper
from django.contrib.auth.models import User

#testing the creation of an Apiary model with corresponding attributes (checking if it was created in the database)
class ApiaryModelTest(TestCase):
    def setUp(self):
        #setting up the model 
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.apiary = Apiary.objects.create(title='Test Apiary', contact_email='test@example.com')
        self.keeper = Keeper.objects.create(name='Test Keeper', email='test@example.com', apiary=self.apiary)

    def test_apiary_creation(self):
        """Test Apiary model creation"""
        #check the database for the object matching the ID
        apiary = Apiary.objects.get(id=self.apiary.id)
        if apiary.title == 'Test Apiary' and apiary.contact_email == 'test@example.com' and apiary.keeper == self.keeper:
            print("                  -----                  ")
            print("Test Apiary model creation: OK")
            print("                  -----                  ")
        else:
            print("                  -----                  ")
            print("Test Apiary model creation: FAILED")
            print("                  -----                  ")

#testing the creation of a Hive model with corresponding attributes (checking if it was created in the database)
class HiveModelTest(TestCase):
    def setUp(self):
        #setting up the model
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.apiary = Apiary.objects.create(title='Test Apiary', contact_email='test@example.com')
        self.keeper = Keeper.objects.create(name='Test Keeper', email='test@example.com', apiary=self.apiary)
        self.hive = Hive.objects.create(title='Test Hive', apiary=self.apiary)

    def test_hive_creation(self):
        """Test Hive model creation"""
        #check the database for the object matching the ID
        hive = Hive.objects.get(id=self.hive.id)
        if hive.title == 'Test Hive' and hive.apiary == self.apiary:
            print("                  -----                  ")
            print("Test Hive model creation: OK")
            print("                  -----                  ")
        else:
            print("                  -----                  ")
            print("Test Hive model creation: FAILED")
            print("                  -----                  ")
