import multiprocessing
import os
from unittest import TestCase
from flask_login import current_user
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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

        self.driver.find_element("id", "1-post-body").click()
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

    def test_user_profile(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        SeleniumTests.post(self, "Test Title", "Test Post", None)

        self.driver.find_element("id", "profile").click()

        profile_picture = self.driver.find_element("id", "profile-picture")
        self.assertTrue(profile_picture is not None)

        username = self.driver.find_element("id", "user-username")
        self.assertTrue(username.get_attribute("innerHTML") == "susan")

        last_active = self.driver.find_element("id", "user-lastactive")
        self.assertTrue(last_active is not None)

        edit_profile_button = self.driver.find_element("id", "edit-profile")
        self.assertTrue(edit_profile_button is not None)

        post_count = self.driver.find_element("id", "post-count")
        self.assertTrue(post_count.get_attribute("innerHTML") == "1 Post:") 

        author_picture = self.driver.find_element("id", "1-author-picture")
        self.assertTrue(author_picture is not None)

        post_author = self.driver.find_element("id", "1-post-author")
        self.assertTrue(post_author.get_attribute("innerHTML") == "susan")

        timestamp = self.driver.find_element("id", "1-post-timestamp")
        self.assertTrue(timestamp is not None)

        post_title = self.driver.find_element("id", "1-post-title")
        self.assertTrue(post_title.get_attribute("innerHTML") == "Test Title")

        post_body = self.driver.find_element("id", "1-post-body")
        self.assertTrue(post_body.get_attribute("innerHTML") == "Test Post")

        post_actions = self.driver.find_element("id", "1-post-actions")
        self.assertTrue(post_actions is not None)

    def test_edit_profile(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")

        self.driver.find_element("id", "profile").click()
        self.driver.find_element("id", "edit-profile").click()

        self.driver.find_element("id", "bio").send_keys("Test bio")
        self.driver.find_element("id", "submit-profile").click()

        bio = self.driver.find_element("id", "user-bio")
        self.assertTrue(bio.get_attribute("innerHTML") == "Test bio")
    
    def test_search(self):
        SeleniumTests.register(self, "susan", "susan@gmail.com", "cat")
        SeleniumTests.login(self, "susan", "cat")
        SeleniumTests.post(self, "Test1", "Test Post 1", None)
        SeleniumTests.post(self, "Test2", "Test Post 2", None)

        self.driver.find_element("id", "search").send_keys("Test1")
        self.driver.find_element("id", "submit-search").click()

        results = self.driver.find_elements(By.CLASS_NAME, "post")
        self.assertTrue(len(results) == 1)
        result_title = results[0].find_element("id", "1-post-title")
        self.assertTrue(result_title.get_attribute("innerHTML") == "Test1")








    











        #Plan
        #Kelly - make tests for posts, comments, user profile page and edit profile, search













