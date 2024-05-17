import multiprocessing
import os
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from config import TestConfig
import sqlalchemy as sa
from app.models import User, Post, Comment

localHost = "http://localhost:5000/"

class SeleniumTests(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        multiprocessing.set_start_method("fork")
        self.server_thread = multiprocessing.Process(target=self.testApp.run)
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)
    
    def tearDown(self):
        self.server_thread.terminate()
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        login = self.driver.find_element("id", "login")
        self.assertTrue(login.get_attribute("innerHTML") == "Login")
    
    def test_register_and_login(self):
        self.driver.find_element("id", "start-cooking").click()
        self.driver.find_element("id", "username").send_keys("susan")
        self.driver.find_element("id", "email").send_keys("susan@gmail.com")
        self.driver.find_element("id", "password").send_keys("cat")
        self.driver.find_element("id", "password2").send_keys("cat")
        self.driver.find_element("id", "submit").click()
        topnav_home = self.driver.find_element("id", "topnav")
        login_title = self.driver.find_element("id", "sign-in")

        self.assertTrue(topnav_home is not None)
        self.assertTrue(login_title.get_attribute("innerHTML") == "Sign In")

        self.driver.find_element("id", "username").send_keys("susan")
        self.driver.find_element("id", "password").send_keys("cat")
        self.driver.find_element("id", "submit").click()

        topnav_index = self.driver.find_element("id", "topnav")
        hello = self.driver.find_element("id", "hello")
        question = self.driver.find_element("id", "question")

        self.assertTrue(topnav_index is not None)
        self.assertTrue(hello.get_attribute("innerHTML") == "Hi, susan!")
        self.assertTrue(question.get_attribute("innerHTML") == "What would you like to cook?")

    '''
    def test_login(self):
        user = User(username="susan", email="susan@gmail.com")
        user.set_password("cat")
        db.session.add(user)
        db.session.commit()
        
        self.driver.find_element("id", "login").click()
        self.driver.find_element("id", "username").send_keys("susan")
        self.driver.find_element("id", "password").send_keys("cat")
        self.driver.find_element("id", "submit").click()
        topnav = self.driver.find_element("id", "topnav")
        hello = self.driver.find_element("id", "hello")
        question = self.driver.find_element("id", "question")
        
        self.assertTrue(topnav is not None)
        self.assertTrue(hello.get_attribute("innerHTML") == "Hi, susan!")
        self.assertTrue(question.get_attribute("innerHTML") == "What would you like to cook?")
    '''
    















