# Generated by Django 2.2.1 on 2019-05-15 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('cid', models.IntegerField(primary_key=True, serialize=False)),
                ('cname', models.TextField()),
                ('short_cmane', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('pcode', models.TextField()),
                ('brand', models.TextField()),
                ('pname', models.TextField()),
                ('category', models.TextField()),
                ('price', models.IntegerField()),
                ('url', models.URLField()),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Country')),
            ],
        ),
    ]
