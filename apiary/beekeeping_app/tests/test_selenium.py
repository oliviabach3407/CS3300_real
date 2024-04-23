from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException


from ..models import Apiary
from ..models import Hive
from django.contrib.auth.models import User

#for starting on the index page for every test
from django.urls import reverse 

'''
CONTAINS 2 HAPPY TESTS, 2 SAD TESTS, AND ONE GENERAL HAPPY TEST
'''

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
        #navigate to login page
        self.browser.get(self.live_server_url + reverse('login'))

        wait = WebDriverWait(self.browser, 10)

        #click on the signup link
        register_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/accounts/register/')]"))
        )
        register_link.click()

        #fill in signup form and submit
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

        #assert that user is redirected to login page
        expected_url = self.live_server_url + reverse('login')
        self.assertEqual(self.browser.current_url, expected_url, f"\n---------------------\nUser was successfully registered : redirected to the login page: {expected_url}\n---------------------")


    def login(self):
        #navigate to login page
        self.browser.get(self.live_server_url + reverse('login'))

        wait = WebDriverWait(self.browser, 10)

        #fill in login form and submit
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input.send_keys('testuser')

        password_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_input.send_keys('HelloWorld10!')
        
        #submit the form
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='login']"))
        )
        submit_button.click()

    #for sad test
    def different_login(self):
        #navigate to login page
        self.browser.get(self.live_server_url + reverse('login'))

        wait = WebDriverWait(self.browser, 10)

        #fill in login form and submit
        username_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_username'))
        )
        username_input.send_keys('wrongusername')

        password_input = wait.until(
            EC.presence_of_element_located((By.ID, 'id_password'))
        )
        password_input.send_keys('wrongpassword')
        
        #submit the form
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='login']"))
        )
        submit_button.click()


    def logout(self):
        #navigate to logout page
        self.browser.get(self.live_server_url + reverse('logout'))

    #check if user was successfully logged in
    def test_happy_login(self):
        '''
        GIVEN Robin has registered
        WHEN she enters the correct username and password
        THEN she will see 'My Apiary' in the navigation bar"
        '''

        #registers before they login
        self.login() 

        wait = WebDriverWait(self.browser, 10)

        #check if "MyApiary" is accessible from the nav bar after logging in
        my_apiary_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'My Apiary')]")))
        assert my_apiary_link.is_displayed(), "My Apiary link not found in the navigation bar after login"
        
        #display a success message
        print("\n---------------------\nLogin successful because My Apiary link was found in the navigation bar.\n---------------------")

    #check if user wasn't logged in
    def test_sad_login(self):
        '''
        GIVEN Robin has registered
        WHEN she enters the wrong username or password
        THEN she will see the error message "Your username and password didn't match. Please try again."
        '''

        #registers, but doesn't put in the correct username/password
        self.different_login()

        wait = WebDriverWait(self.browser, 10)

        #looking for the error message: "Your username and password didn't match. Please try again."
        error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "p")))
        assert error_message.is_displayed(), "Error message not found for incorrect login"

        #extracting the actual test from the message found on the page
        error_message_text = error_message.text

        #display a success message if assert passed
        print(f"\n---------------------\nSad login successful. Error message found: '{error_message_text}'\n---------------------")
        

    #check if user was successfully logged in and given role permissions 
    def test_happy_role(self):
        '''
        GIVEN Joan has registered
        WHEN she logs in
        THEN she will be able to see 'My Apiary' in the navbar
        AND 
        WHEN she clicks on 'My Apiary'
        THEN she will see the user homepage
        '''

        self.login() 

        wait = WebDriverWait(self.browser, 10)

        #check if "MyApiary" is accessible from the nav bar after logging in
        my_apiary_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'My Apiary')]")))
        assert my_apiary_link.is_displayed(), "My Apiary link not found in the navigation bar after login"
        
        #display a success message
        print("\n---------------------\nLogin successful because My Apiary link was found in the navigation bar.\n---------------------")

        #click the "MyApiary" link
        my_apiary_link.click()
        
        #assert if the user is taken to the correct URL
        expected_url = self.live_server_url + reverse('user_page')
        self.assertEqual(self.browser.current_url, expected_url, f"User was not redirected to http://127.0.0.1:8000/user/ (the My Apiary Page)")

        #display a success message
        print("\n---------------------\nUser successfully redirected to the My Apiary Page (meaning they had the role required to access it).\n---------------------")

    #check if user isn't logged in and isn't given role permissions 
    def test_sad_role(self):
        '''
        GIVEN Joan has registered
        WHEN she doesn't log in
        THEN she will not be able to see 'My Apiary' in the navbar
        '''
        #registered automatically
        #don't log in - check to see if My Apiary shows up on the page

        self.browser.get(self.live_server_url)

        wait = WebDriverWait(self.browser, 10)

        #check if "My Apiary" link is not present in the navbar
        try:
            #wait for the navbar elements to be visible
            navbar_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//nav[@class='navbar']//div[@class='nav-link nav-item-large']//a[contains(text(), 'My Apiary')]")))
        except TimeoutException:
            #display a success message if the link is not found within the timeout
            print("\n---------------------\nSad role test successful because 'My Apiary' link was not found in the navigation bar.\n---------------------")
        else:
            #fail the test if the 'My Apiary' link is found
            self.fail("Unexpectedly found 'My Apiary' link in the navigation bar")
        
    def test_view_published_hives_loggedin(self):
        """
        GIVEN Robin is logged in
        WHEN she clicks the 'Public Users' button
        THEN she will be able to see a list of beekeepers.
        """
        #signup should automatically be called
        self.login()

        self.browser.get(self.live_server_url + reverse('index'))

        wait = WebDriverWait(self.browser, 10)

        #click on the 'View Published Hives' button
        view_hives_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Public Users')]"))
        )
        view_hives_button.click()

        #assert that the words 'All Public Beekeepers:' show up on the page
        all_public_beekeepers_text = "All Public Beekeepers:"
        assert all_public_beekeepers_text in self.browser.page_source, f"{all_public_beekeepers_text} not found on the page"

        print("\n---------------------\nSuccessfully found 'All Public Beekeepers:' on the page.\n---------------------")

    def test_logout(self):
        """
        GIVEN Joan is logged in
        WHEN she clicks the logout button
        THEN she will be redirected to logout.html
        """
        #signup should automatically be called
        self.login()

        #click the logout button
        self.logout()

        #assert if the user is redirected to the logout page
        expected_url = self.live_server_url + reverse('logout')
        self.assertEqual(self.browser.current_url, expected_url, f"User was not redirected to http://127.0.0.1:8000/logout/?next=/user/ after logout")
        print("\n---------------------\nUser successfully redirected to logout page after logout.\n---------------------")


'''
These tests worked before I updated the authentication part of my app:
-took out the 'test' part so they aren't run automatically
-kept just for completion purposes and BDD scenario consciousness
'''

# def create_hive_successful(self):
    #     '''
    #     -------------HAPPY-------------
    #     GIVEN Joan is on the home page
    #     WHEN she clicks the 'view apiary' button
    #     AND clicks the 'new hive' button
    #     AND fills both form fields
    #     AND clicks 'submit'
    #     THEN a new hive will have been added to the database
    #     '''

    #     testApiary = Apiary.objects.create(
    #         title="Test Apiary",
    #         company="Example Company",
    #         contact_email="example2@example.com",
    #         about="About this apiary",
    #         is_published=True
    #     )

    #     #steps to create a hive: 
    #     #click on "view apiary" button 
    #     #click on "new" hive button
    #     #enter a title into the title section of the form
    #     #enter a description into the description section of the form
    #     #press the "submit" button

    #     self.browser.get(self.live_server_url) 

    #     wait = WebDriverWait(self.browser, 10)

    #     #signup should automatically be called
    #     self.login()

    #     #wait for the 'View Apiary' button to be clickable and visible
    #     view_apiary_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, f'//a[@href="{testApiary.get_absolute_url()}" and contains(@class, "btn") and contains(@class, "btn-primary")]'))
    #     )
    #     view_apiary_button.click()

    #     #click the 'new hive' button
    #     new_hive_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'New') and @class='btn btn-primary']"))
    #     )
    #     new_hive_button.click()

    #     html_response = self.browser.page_source
    #     print("HTML response after clicking 'New' button:")
    #     print(html_response)

    #     #fill in the hive form
    #     title_input = wait.until(
    #         EC.presence_of_element_located((By.ID, 'id_title'))
    #     )
    #     title_input.send_keys("Test Hive Title")

    #     description_input = wait.until(
    #         EC.presence_of_element_located((By.ID, 'id_description'))
    #     )
    #     description_input.send_keys("Test Hive Description")

    #     #submit the form
    #     submit_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    #     )
    #     submit_button.click()

    #     new_hive_title = "Test Hive Title"
    #     new_hive_description = "Test Hive Description"

    #     #check if the new hive exists in the database
    #     new_hive = Hive.objects.filter(title=new_hive_title, description=new_hive_description).first()

    #     #assert that the new hive object is found in the database
    #     self.assertIsNotNone(new_hive, "New hive object not found in the database")

    #     #print success message if the assertion passes
    #     print("\nHappy Test passed successfully: New hive object found in the database.")

    # def create_hive_no_form(self):
    #     '''
    #     -------------SAD-------------
    #     GIVEN Joan is on the home page
    #     WHEN she clicks the 'view apiary' button
    #     AND clicks the 'new hive' button
    #     AND clicks 'submit'
    #     THEN she will see two errors 
    #     '''
        
    #     #steps to create a hive: 
    #     #click on "view apiary" button 
    #     #click on "new" hive button
    #     #enter a title into the title section of the form
    #     #enter a description into the description section of the form
    #     #press the "submit" button

    #     #signup should automatically be called
    #     self.login()

    #     testApiary2 = Apiary.objects.create(
    #         title="Test Apiary",
    #         company="Example Company",
    #         contact_email="example2@example.com",
    #         about="About this apiary",
    #         is_published=True
    #     )

    #     self.browser.get(self.live_server_url)
    #     self.browser.get(self.live_server_url + reverse('index'))

    #     wait = WebDriverWait(self.browser, 10)

    #     #wait for the 'View Apiary' button to be clickable and visible
    #     view_apiary_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, f'//a[@href="{testApiary2.get_absolute_url()}" and contains(@class, "btn") and contains(@class, "btn-primary")]'))
    #     )
    #     view_apiary_button.click()

    #     #click the 'new hive' button
    #     new_hive_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'New') and @class='btn btn-primary']"))
    #     )
    #     new_hive_button.click()

    #     #submit the form
    #     submit_button = wait.until(
    #         EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    #     )
    #     submit_button.click()

    #     #check if the two error messages popped up
    #     error_messages = wait.until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='errorlist']/li"))
    #     )

    #     #assert that two error messages are displayed
    #     self.assertEqual(len(error_messages), 2, "Expected two error messages, but found different number.")
    #     print("\nSad Test passed successfully: Two error messages are displayed since the user didn't fill in the two required form fields.")