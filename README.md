# Secret Santa

App represents MVP of Secret Santa site.

It allows users to:

1. Organize and manage "Secret Santa" games
2. Invite other players
3. Perform draws manually or automatically on game draw dates
4. Set player pairs exclusions

![secret santa](https://i.ibb.co/RT6cjzX/readme.jpg)

## Development mode

### Install

At least Python3.8 and Git should be already installed.

1. Clone the repository
```
git clone https://github.com/balancy/secret_santa.git
```

2. Go inside cloned repo and activate virtual environment

```
cd secret_santa
```

```
python -m venv .venv
```

```
. .venv/bin/activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and define your environment variables

```
cp .env.example .env
```

- `BITLY_TOKEN` - your [bitly](https://app.bitly.com/settings/api/) token
- `DEFAULT_FROM_EMAIL` - your server email for players to receive messages from
- `EMAIL_HOST`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_PORT` - see [documentation](https://docs.djangoproject.com/en/4.0/topics/email/) for all `EMAIL` variables

5. Migrate the database
```
python manage.py migrate
```

6. Create superuser

```
python manage.py createsuperuser
```

7. Add the cron job to your crontab by executing bash command:

```
(crontab -l ; echo "59 23 * * * python3 /full_path_to_your_manage_py_script/manage.py draw") | crontab -
```

- `full_path_to_your_manage_py_script`  - full path to your manage.py script location


### Launch the app

```
python manage.py runserver
```

Your app will be available on [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Production mode

At least Python3.8, Git, Docker and docker-compose should already be installed.

1. Clone the repository

```
git clone https://github.com/balancy/secret_santa.git
```

2. Go inside cloned repo

```
cd secret_santa
```

3. Copy `.env.prod.example` to `.env.prod` and define your environment variables

```
cp .env.prod.example .env.prod
```

- `ALLOWED_HOSTS` - see [documentation](https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts) for details
- `BITLY_TOKEN` - your [bitly](https://app.bitly.com/settings/api/) token
- `DEFAULT_FROM_EMAIL` - your server email for players to receive messages from
- `EMAIL_HOST`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_PORT` - see [documentation](https://docs.djangoproject.com/en/4.0/topics/email/) for all `EMAIL` variables
- `HASH_KEY` - some random string used for hashing game ids
- `POSTGRES_DB` - your db name
- `POSTGRES_PASSWORD` - your db password
- `POSTGRES_USER` - your db username
- `SECRET_KEY` - django project secret key

4. Run deployment script

```
./deployment_script.sh
```

5. Create superuser

```
sudo docker exec -it secret_santa_django_1 python manage.py createsuperuser
```

6. Create [nginx config](https://sayari3.com/articles/11-how-to-serve-djangos-static-files-using-nginx-on-localhost/) to serve static

7. Add current user to crontab group and Add the cron job to your crontab

```
sudo usermod -a -G crontab "$USER"
```

```
(crontab -l ; echo "59 23 * * * sudo docker exec -t secret_santa_django_1 python manage.py draw") | crontab -
```

8. Your app will be available on `90` port
