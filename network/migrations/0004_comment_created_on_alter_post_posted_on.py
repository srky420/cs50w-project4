# Generated by Django 4.2.2 on 2023-06-13 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_follower_follower_alter_post_posted_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 13, 21, 28, 45, 856790)),
        ),
        migrations.AlterField(
            model_name='post',
            name='posted_on',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 13, 21, 28, 45, 855792)),
        ),
    ]
