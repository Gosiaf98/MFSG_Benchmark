# Generated by Django 3.1.4 on 2021-01-05 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
                ('dom', models.IntegerField(default=0)),
                ('first_byte', models.IntegerField(default=0)),
            ],
        ),
    ]
