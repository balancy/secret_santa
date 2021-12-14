# Generated by Django 4.0 on 2021-12-14 17:33

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='название')),
                ('max_price', models.PositiveIntegerField(verbose_name='максимальная стоимость подарка')),
                ('draw_date', models.DateTimeField(verbose_name='Дата жеребьёвки')),
                ('gift_date', models.DateTimeField(verbose_name='Дата отправки подарка')),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games_coordinators', to='games.customuser', verbose_name='организатор')),
            ],
            options={
                'verbose_name': 'игра',
                'verbose_name_plural': 'игры',
            },
        ),
        migrations.CreateModel(
            name='Santa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlist', models.TextField(null=True, verbose_name='Желания')),
                ('letter_to_santa', models.TextField(null=True, verbose_name='Письмо Санте')),
                ('game', models.ManyToManyField(related_name='santas', to='games.Game', verbose_name='игра')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='games.customuser')),
            ],
            options={
                'verbose_name': 'санта',
                'verbose_name_plural': 'санты',
            },
        ),
        migrations.CreateModel(
            name='Draw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='draws', to='games.game', verbose_name='игра')),
                ('giver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='draws_givers', to='games.santa', verbose_name='даритель')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='draws_receivers', to='games.santa', verbose_name='одаряемый')),
            ],
            options={
                'verbose_name': 'жеребьёвка',
                'verbose_name_plural': 'жеребьёвки',
            },
        ),
    ]
