# Generated by Django 3.0.4 on 2020-03-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200311_0709'),
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collaborator',
            name='skill',
        ),
        migrations.AddField(
            model_name='collaborator',
            name='skill',
            field=models.ManyToManyField(related_name='creative_type', to='accounts.Skill'),
        ),
        migrations.RemoveField(
            model_name='showcase',
            name='skill_type',
        ),
        migrations.AddField(
            model_name='showcase',
            name='skill_type',
            field=models.ManyToManyField(to='accounts.Skill'),
        ),
    ]
