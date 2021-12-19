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
smtp_host="smtp.youdomain.com"
smtp_port="25"
mail_server_login="login"
mail_server_password="password"
from_adress="you@youdomain.com"
use_tls=True
```
If your smtp server use SSL set use_ssl to True or False if not.

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

6. Create santa card for superuser

```
sudo docker exec -it secret_santa_django_1 python manage.py create_santas_for_users
```

7. Create [nginx config](https://sayari3.com/articles/11-how-to-serve-djangos-static-files-using-nginx-on-localhost/) for serving static