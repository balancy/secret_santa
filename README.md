# Secret Santa

## Install

At least Python3.8 and Git should be already installed.

1. Clone the repository
```
git clone git@github.com:balancy/secret_santa.git
```

2. Go inside cloned repo, install depenencies and activate virtual environment
```
cd secret_santa
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

3. Rename `.env.example` to `.env` and change `SECRET_KEY` environment variable

- `SECRET_KEY`  - django secret key

4. Migrate the database
```
python manage.py migrate
```

## Launch the app

```
python manage.py runserver
```
