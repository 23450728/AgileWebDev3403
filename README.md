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

How to run the flask environment:

run the following in the terminal (use export on mac, use set on windows):
docker run --name elasticsearch -d --rm -p 9200:9200 --memory="2GB" -e discovery.type=single-node -e xpack.security.enabled=false -t docker.elastic.co/elasticsearch/elasticsearch:8.13.0
export ELASTICSEARCH_URL=http://localhost:9200/
flask run

If you would like to enable email support, type the following into your terminal:
export MAIL_SERVER=localhost
export MAIL_PORT=8025
export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=<your-gmail-username>
export MAIL_PASSWORD=<your-gmail-password>

If you would like to enable testing:
python -m unittest seleniumtests.py
python -m unittest unittests.py
