# Generated by Django 4.0.8 on 2022-10-24 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_userprofile_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='posts',
            field=models.ManyToManyField(default=None, to='core.post'),
        ),
    ]
