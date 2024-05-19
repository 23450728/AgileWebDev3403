Title - What To Cook?

Description - Ever want to know what to cook, or how to cook it?
We have designed an interactive and easy to use forum for you to find exactly what you woulkd like to cook.

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

If you would like to enable email support, type the following into your terminal:<br />
export MAIL_SERVER=localhost<br />
export MAIL_PORT=8025<br />
export MAIL_SERVER=smtp.googlemail.com<br />
export MAIL_PORT=587<br />
export MAIL_USE_TLS=1<br />
export MAIL_USERNAME=<your-gmail-username><br />
export MAIL_PASSWORD=<your-gmail-password><br />

If you would like to enable testing:<br />
python -m unittest seleniumtests.py<br />
python -m unittest unittests.py<br />
