# Generated by Django 4.2.3 on 2023-11-02 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank_app', '0003_alter_regmodel_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='regmodel',
            name='ac_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
