# Generated by Django 4.2.3 on 2023-10-25 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='regmodel',
            name='img',
            field=models.FileField(upload_to='bank_app/static/images'),
        ),
    ]
