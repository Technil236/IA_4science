# Generated by Django 4.2.6 on 2023-10-23 19:42

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_birthday_alter_user_pseudonym'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='pseudonym',
            field=models.CharField(default=accounts.models.generate_pseudonym, max_length=250, unique=True, verbose_name='Pseudonyme'),
        ),
    ]
