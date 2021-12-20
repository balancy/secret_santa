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
(crontab -l ; echo "59 23 * * * python3 /full_path_to_your_manage_py_script/manage.py draw") | crontab -
```
Change **full_path_to_your_manage_py_script** to the full path to your manage.py script location.

4. Create .env file in project folder and add your SMTP server's settings:
```
EMAIL_HOST=smtp.youdomain.com
EMAIL_PORT=25
EMAIL_HOST_USER=login
EMAIL_HOST_PASSWORD=password
DEFAULT_FROM_EMAIL=you@youdomain.com
EMAIL_USE_TLS=True
BITLY_TOKEN=123344
```
How to get token [see bitly docs](https://bitly.com/a/sign_in?rd=/settings/api/)

If your smtp server use TLS set EMAIL_USE_TLS to True or False if not.

## Launch the app

```
python manage.py runserver
```

## Production

Docker, docker-compose should already be installed.

1. Clone the repository

```
git clone git@github.com:balancy/secret_santa.git
```

2. Create .env.prod file

<!---TODO-->

3. Build images

```
sudo docker-compose build
```

4. Run containers

```
sudo docker-compose up -d
```

5. Create superuser

```
sudo docker exec -it secret_santa_django_1 python manage.py createsuperuser
```

6. Create [nginx config](https://sayari3.com/articles/11-how-to-serve-djangos-static-files-using-nginx-on-localhost/) for serving static
