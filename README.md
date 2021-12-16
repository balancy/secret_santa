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

3. Migrate the database
```
python manage.py migrate
```

4. Add the cron job to your crontab by executing bash command:
```
(crontab -l ; echo "59 23 * * * /full_path_to_your_manage_py_script/python3 manage.py draw") | crontab -
```
Change **full_path_to_your_manage_py_script** to the full path to your manage.py script location.

## Launch the app

```
python manage.py runserver
```
