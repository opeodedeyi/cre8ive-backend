# Generated by Django 3.0.4 on 2020-06-15 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0003_auto_20200511_0308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='showcase',
            name='assets',
        ),
        migrations.AddField(
            model_name='showcase',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]