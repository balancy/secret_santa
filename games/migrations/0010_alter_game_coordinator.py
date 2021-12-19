# Generated by Django 4.0 on 2021-12-19 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0009_alter_game_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='coordinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='games', to='games.customuser', verbose_name='организатор'),
        ),
    ]