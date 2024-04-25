from django.test import TestCase
#C:\Users\olivi\OneDrive\GitHub\CS3300_real\apiary\beekeeping_app\forms.py
from beekeeping_app.forms import HiveForm

class BeekeepingAppTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("                  -----                  ")
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        print("                  -----                  ")
        pass

    def setUp(self):
        print("                  -----                  ")
        print("setUp: Run once for every test method to set up clean data.")
        print("                  -----                  ")
        pass

    #runs to test if the hive form is being filled and populating the database
    def test_hive_form_valid(self):
        """Test HiveForm with valid data"""
        form_data = {'title': 'Test Hive', 'description': 'Test Description'}
        form = HiveForm(data=form_data)
        if form.is_valid():
            print("Test HiveForm with valid data: OK - Form is valid.")
        else:
            print("Test HiveForm with valid data: FAILED - Form is not valid.")

    #runs to test if the hive form is NOT being filled and NOT populating the database
    def test_hive_form_invalid(self):
        """Test HiveForm with invalid data"""
        form_data = {'title': '', 'description': 'Test Description'}
        form = HiveForm(data=form_data)
        if not form.is_valid():
            print("Test HiveForm with invalid data: OK - Form is invalid.")
        else:
            print("Test HiveForm with invalid data: FAILED - Form is valid.")
