# Generated by Django 3.0.4 on 2020-06-15 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0004_auto_20200615_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(blank=True, null=True, upload_to='')),
                ('showcase_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias_showcase', to='showcase.Showcase')),
            ],
        ),
    ]
