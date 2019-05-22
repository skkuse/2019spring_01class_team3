# Generated by Django 2.2.1 on 2019-05-22 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_favorite_kprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='pid',
        ),
        migrations.AddField(
            model_name='product',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='favorite',
            name='kprice',
            field=models.TextField(),
        ),
    ]
