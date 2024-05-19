Title - What To Cook?

Description:
Ever want to know what to cook or how to cook it? We have designed an interactive and easy to use forum, What to Cook?, for you to find cooking inspiration and tips. Simply make posts to ask questions and our passionate foodie community can reply to share their cooking advice. Our application contains the following main functionalities and the relevant instructions are also shown below.

| Student ID        | Full Name               | GITHUB name  |
| ------------------|:-----------------------:| ------------:|
| 23450728          | Chester Chatfield       | 23450728     |
| 23614821          | Kelly Snow              | kksnowy      |
| 23341388          | Alithea Low             | alxth3a      |
| 23333163          | Sona Jimson             | Sonj03       |

Group Members: 23450728

How to run the flask environment:<br />
run the following in the terminal (use export on mac, use set on windows):<br />
<br />
docker run --name elasticsearch -d --rm -p 9200:9200 --memory="2GB" -e discovery.type=single-node -e xpack.security.enabled=false -t docker.elastic.co/elasticsearch/elasticsearch:8.13.0<br />
export ELASTICSEARCH_URL=http://localhost:9200/<br />
flask run<br />

Running the DB for the first time:<br/>
flask db upgrade<br/>
flask db migrate<br/>
flask db upgrade<br/>

If you would like to enable email support, type the following into your terminal:<br />
export MAIL_SERVER=localhost<br />
export MAIL_PORT=8025<br />
export MAIL_SERVER=smtp.googlemail.com<br />
export MAIL_PORT=587<br />
export MAIL_USE_TLS=1<br />
export MAIL_USERNAME=your-gmail-username<br />
export MAIL_PASSWORD=your-gmail-password<br />

If you would like to enable testing:<br />
python -m unittest seleniumtests.py<br />
python -m unittest unittests.py<br />

How to use our application:

Description:
Ever want to know what to cook or how to cook it? We have designed an interactive and easy to use forum, What to Cook?, for you to find cooking inspiration and tips. Simply make posts to ask questions and our passionate foodie community can reply to share their cooking advice. Our application contains the following main functionalities and the relevant instructions are also shown below.

Register and login:
	1. When you launch What to Cook?, you are immediately taken to the home page. Click "Start Cooking!" which will take you to a registration page.
	2. Enter your details to make an account.
	3. After registering, you are taken to the sign-in page. Enter your details and click "Submit". You are then taken to the explore page ad you are ready to browse!
	4. When finished, you can logout by clicking the right most icon in top navigation bar.

NOTE: You can also use What to Cook? without having an account but only limited functionalities will be available (e.g. you cannot make a post or comment).

Make a post:
	1. If you're logged in, you can make a post by clicking the + icon in the top navigation bar.
	2. Enter a title, type your post, and attach an image saved on your computer if you like. Click "Submit" and your post will be visible in the explore page.

Make a comment:
	1. If you're logged in, you can make a comment by clicking the speech bubble inside a post. This takes you to a comment page
	2. Enter your comment and click "Submit". This takes you to a separate screen displaying only the post and your comment underneath it (along with any other existing comments)

Search for a post or user:
	1. In the search bar located in the top navigation bar, type keywords of a post or a username you would like to search. Press the "enter" key. The posts with the matching keyword or username would appear as the search results.

View your user page:
	1. Each user has a page showing their profile and all the posts that they've created. Click on the user icon in the top navigation to view yours.
	2. You can also view other users' page by clicking on a username in a post.

Edit your profile:
	1. Click on the "Edit Profile" button in your user page. This takes you to a page where you can change your username, email, and bio.


References:
Migeul Grinberg Flask Tutorial Blog: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
Miguel Grinberg Flask Image upload: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
CHATGPT 3.5 and 4.0
