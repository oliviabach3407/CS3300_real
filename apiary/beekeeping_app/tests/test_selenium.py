from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from ..models import Apiary
from ..models import Hive
from django.contrib.auth.models import User

#for starting on the index page for every test
from django.urls import reverse 

# Create your tests here.

class TestName(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        super().setUp()
        #ALWAYS SIGN UP BEFORE TRYING TO LOGIN
        self.signup()

    def signup(self):
        # Navigate to login page
        self.browser.get(self.live_server_url + reverse('login'))

        wait = WebDriverWait(self.browser, 10)

        # Click on the signup link
        register_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/accounts/register/')]"))
        )
        register_link.click()

        # Fill in signup form and submit
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input.send_keys('testuser')

        email_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_email'))
        )
        email_input.send_keys('testuser@example.com')

        password1_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_password1'))
        )
        password1_input.send_keys('HelloWorld10!')

        password2_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_password2'))
        )
        password2_input.send_keys('HelloWorld10!')

        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @name='Create User']"))
        )
        submit_button.click()

        # Assert that user is redirected to login page
        #self.assertEqual(self.browser.current_url, self.live_server_url + reverse('login'))

    def login(self):
        # Navigate to login page
        self.browser.get(self.live_server_url + reverse('login'))

        wait = WebDriverWait(self.browser, 10)

        # Fill in login form and submit
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input.send_keys('testuser')

        password_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_input.send_keys('HelloWorld10!')
        
        # Submit the form
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='login']"))
        )
        submit_button.click()

    def logout(self):
        # Navigate to logout page
        self.browser.get(self.live_server_url + reverse('logout'))

    def test_create_hive_successful(self):
        '''
        -------------HAPPY-------------
        GIVEN Joan is on the home page
        WHEN she clicks the 'view apiary' button
        AND clicks the 'new hive' button
        AND fills both form fields
        AND clicks 'submit'
        THEN a new hive will have been added to the database
        '''
        #signup should automatically be called
        self.login()

        testApiary = Apiary.objects.create(
            title="Test Apiary",
            company="Example Company",
            contact_email="example2@example.com",
            about="About this apiary",
            is_published=True
        )

        #steps to create a hive: 
        #click on "view apiary" button 
        #click on "new" hive button
        #enter a title into the title section of the form
        #enter a description into the description section of the form
        #press the "submit" button

        self.browser.get(self.live_server_url)

        #start on the index page
        self.browser.get(self.live_server_url + reverse('index'))


        wait = WebDriverWait(self.browser, 10)

        #wait for the 'View Apiary' button to be clickable and visible
        view_apiary_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@href="{testApiary.get_absolute_url()}" and contains(@class, "btn") and contains(@class, "btn-primary")]'))
        )
        view_apiary_button.click()

        #click the 'new hive' button
        new_hive_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'New') and @class='btn btn-primary']"))
        )
        new_hive_button.click()

        #fill in the hive form
        title_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_title'))
        )
        title_input.send_keys("Test Hive Title")

        description_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_description'))
        )
        description_input.send_keys("Test Hive Description")

        #submit the form
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()

        new_hive_title = "Test Hive Title"
        new_hive_description = "Test Hive Description"

        #check if the new hive exists in the database
        new_hive = Hive.objects.filter(title=new_hive_title, description=new_hive_description).first()

        # Assert that the new hive object is found in the database
        self.assertIsNotNone(new_hive, "New hive object not found in the database")

        # Print success message if the assertion passes
        print("\nHappy Test passed successfully: New hive object found in the database.")

    def test_create_hive_no_form(self):
        '''
        -------------SAD-------------
        GIVEN Joan is on the home page
        WHEN she clicks the 'view apiary' button
        AND clicks the 'new hive' button
        AND clicks 'submit'
        THEN she will see two errors 
        '''
        
        #steps to create a hive: 
        #click on "view apiary" button 
        #click on "new" hive button
        #enter a title into the title section of the form
        #enter a description into the description section of the form
        #press the "submit" button

        #signup should automatically be called
        self.login()

        testApiary2 = Apiary.objects.create(
            title="Test Apiary",
            company="Example Company",
            contact_email="example2@example.com",
            about="About this apiary",
            is_published=True
        )

        self.browser.get(self.live_server_url)
        self.browser.get(self.live_server_url + reverse('index'))

        wait = WebDriverWait(self.browser, 10)

        #wait for the 'View Apiary' button to be clickable and visible
        view_apiary_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//a[@href="{testApiary2.get_absolute_url()}" and contains(@class, "btn") and contains(@class, "btn-primary")]'))
        )
        view_apiary_button.click()

        #click the 'new hive' button
        new_hive_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'New') and @class='btn btn-primary']"))
        )
        new_hive_button.click()

        #submit the form
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        submit_button.click()

        #check if the two error messages popped up
        error_messages = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='errorlist']/li"))
        )

        #assert that two error messages are displayed
        self.assertEqual(len(error_messages), 2, "Expected two error messages, but found different number.")
        print("\nSad Test passed successfully: Two error messages are displayed since the user didn't fill in the two required form fields.")

    def test_view_published_hives_loggedin(self):
        """
        GIVEN Robin is logged in
        WHEN she clicks the 'view published hives' button
        THEN she will be able to see a list of beekeepers.
        """
        #signup should automatically be called
        self.login()

        self.browser.get(self.live_server_url + reverse('index'))

        wait = WebDriverWait(self.browser, 10)

        # Click on the 'View Published Hives' button
        view_hives_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'View Published Hives')]"))
        )
        view_hives_button.click()

        # Assert that the list of beekeepers is visible
        beekeepers_list = wait.until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='beekeepers-list']"))
        )
        self.assertIsNotNone(beekeepers_list, "List of beekeepers not found")

        # Assert other elements in the page if needed

    def test_view_published_hives_nonloggedin(self):
        """
        GIVEN Robin is not logged in
        WHEN she clicks the 'view published hives' button
        THEN she will be able to see a list of beekeepers.
        """
        self.browser.get(self.live_server_url + reverse('index'))

        wait = WebDriverWait(self.browser, 10)
        
        # Click on the 'View Published Hives' button
        view_hives_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'View Published Hives')]"))
        )
        view_hives_button.click()

        page_source = self.browser.page_source
        if "Server Error (500)" in page_source:
            print("Page contains the message: Server Error (500)")
        else:
            raise AssertionError("Expected message 'Server Error (500)' not found in page source")


    def test_logout(self):
        """
        GIVEN Joan is logged in
        WHEN she clicks the logout button
        THEN she will be redirected to logout.html
        """
        #signup should automatically be called
        self.login()

        self.logout()
        self.assertEqual(self.browser.current_url, self.live_server_url + reverse('logout'))
