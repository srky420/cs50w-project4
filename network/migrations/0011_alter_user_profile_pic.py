# Generated by Django 4.2.2 on 2023-06-23 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(default='images/default-profile-pic.jpg', upload_to='images/'),
        ),
    ]