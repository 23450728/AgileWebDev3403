import multiprocessing
import os
from unittest import TestCase
from flask_login import current_user
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from app import create_app, db
from config import TestConfig
import sqlalchemy as sa
from app.models import User, Post, Comment

localHost = "http://localhost:5000/"
multiprocessing.set_start_method("fork")

class SeleniumTests(TestCase):

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

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
    
    def register(self, username, email, password):
        self.driver.find_element("id", "start-cooking").click()
        self.driver.find_element("id", "username").send_keys(username)
        self.driver.find_element("id", "email").send_keys(email)
        self.driver.find_element("id", "password").send_keys(password)
        self.driver.find_element("id", "password2").send_keys(password)
        self.driver.find_element("id", "submit").click()

    def login(self, username, password):
        self.driver.find_element("id", "username").send_keys(username)
        self.driver.find_element("id", "password").send_keys(password)
        self.driver.find_element("id", "submit-credentials").click()

    def post(self, title, text, image_file):
        self.driver.find_element("id", "make-post").click()
        self.driver.find_element("id", "title").send_keys(title)

        if image_file is not None:
            self.driver.find_element("id", "file").send_keys(os.path.abspath(image_file))

        self.driver.find_element("id", "post").send_keys(text)
        self.driver.find_element("id", "submit-post").click()
        
    def test_register(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        topnav = self.driver.find_element("id", "topnav")
        login_title = self.driver.find_element("id", "sign-in")

        self.assertTrue(topnav is not None)
        self.assertTrue(login_title.get_attribute("innerHTML") == "Sign In")

    def test_login(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        topnav = self.driver.find_element("id", "topnav")
        hello = self.driver.find_element("id", "hello")
        question = self.driver.find_element("id", "question")
        
        self.assertTrue(topnav is not None)
        self.assertTrue(hello.get_attribute("innerHTML") == "Hi, susan!")
        self.assertTrue(question.get_attribute("innerHTML") == "What would you like to cook?")

    def test_logout(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        self.driver.find_element("id", "logout").click()
        start_cooking_button = self.driver.find_element("id", "start-cooking")
        self.assertTrue(start_cooking_button is not None)

    def test_post(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        SeleniumTests.post(self, "Test Title", "Test Post", "test_image.jpg")
        
        author_picture = self.driver.find_element("id", "1-author-picture")
        self.assertTrue(author_picture is not None)

        post_author = self.driver.find_element("id", "1-post-author")
        self.assertTrue(post_author.get_attribute("innerHTML") == "chef/susan")

        timestamp = self.driver.find_element("id", "1-timestamp")
        self.assertTrue(timestamp is not None)

        post_title = self.driver.find_element("id", "1-post-title")
        self.assertTrue(post_title.get_attribute("innerHTML") == "Test Title")

        post_body = self.driver.find_element("id", "1-post-body")
        self.assertTrue(post_body.get_attribute("innerHTML") == "Test Post")

        post_actions = self.driver.find_element("id", "1-post-actions")
        self.assertTrue(post_actions is not None)

        image = self.driver.find_element("id", "1-image")
        self.assertTrue(image is not None)

    def test_comment(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        SeleniumTests.post(self, "Test Title", "Test Post", None)

        self.driver.find_element("id", "1-post").click()
        self.driver.find_element("id", "make-comment").click()
        self.driver.find_element("id", "comment").send_keys("Test Comment")
        self.driver.find_element("id", "submit-comment").click()

        author_picture = self.driver.find_element("id", "1-author-picture")
        self.assertTrue(author_picture is not None)

        post_author = self.driver.find_element("id", "1-post-author")
        self.assertTrue(post_author.get_attribute("innerHTML") == "chef/susan")

        timestamp = self.driver.find_element("id", "1-post-timestamp")
        self.assertTrue(timestamp is not None)

        post_title = self.driver.find_element("id", "1-post-title")
        self.assertTrue(post_title.get_attribute("innerHTML") == "Test Title")

        post_body = self.driver.find_element("id", "1-post-body")
        self.assertTrue(post_body.get_attribute("innerHTML") == "Test Post")

        post_actions = self.driver.find_element("id", "1-post-actions")
        self.assertTrue(post_actions is not None)

        comment_author_picture = self.driver.find_element("id", "1-comment-author-picture")
        self.assertTrue(comment_author_picture is not None)

        comment_author = self.driver.find_element("id", "1-comment-author")
        self.assertTrue(comment_author.get_attribute("innerHTML") == "susan")

        comment_text = self.driver.find_element("id", "1-comment-text")
        self.assertTrue(comment_text.get_attribute("innerHTML") == "Test Comment")

        comment_timestamp = self.driver.find_element("id", "1-comment-timestamp")
        self.assertTrue(comment_timestamp is not None)

    def test_user_profile(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")

        self.driver.find_element("id", "profile").click()
        




    











        #Plan
        #Kelly - make tests for posts, comments, user profile page and edit profile, search













