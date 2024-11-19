# Donation tracking system

## get started

make sure you have python installed in you system

clone the repository

```bash
git clone
cd project
```

setup virtual environment and activate it

```bash
python -m venv venv

source ./venv/Scripts/activate # git bash windows
.\venv\Scripts\activate # powershell
```

install the dependencies

```bash
pip install -r requirements.txt
```

clone the example env file

```bash
# clone .env.example
cp .env.example .env
```
then fill in the values
go the stripe dashboard and get them https://dashboard.stripe.com/test/apikeys

and also add the appropriate postgresql credentials

run the migration

```bash
python manage.py migrate
```

create superuser
```bash
python manage.py createsuperuser
```

and the run the server

```bash
python manage.py runserver
```

remember to setup stripe cli https://docs.stripe.com/stripe-cli

```bash
stripe listen --forward-to localhost:8000/donation/payment/webhook/
```
