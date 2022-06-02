# job-portal-api

virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt

cp .env-sample .env

./manage.py runserver
