# Generated by Django 2.2.6 on 2019-11-12 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_eventos', '0025_mensagem_eventoid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensagem',
            name='participantId',
        ),
    ]