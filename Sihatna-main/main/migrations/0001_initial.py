# Generated by Django 4.2.6 on 2023-10-24 11:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=400, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='forums')),
            ],
            options={
                'verbose_name_plural': 'forums',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('slug', models.SlugField(max_length=400)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('approuved', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.forum')),
            ],
        ),
    ]