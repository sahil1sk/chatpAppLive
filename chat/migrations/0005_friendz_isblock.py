# Generated by Django 3.0.7 on 2020-07-18 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_friendz'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendz',
            name='isblock',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
