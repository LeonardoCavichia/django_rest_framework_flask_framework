# Generated by Django 2.2.6 on 2019-10-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_eventos', '0004_auto_20191017_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='birthdate',
            field=models.DateField(),
        ),
    ]
