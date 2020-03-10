# Generated by Django 3.0.4 on 2020-03-10 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('picture', models.TextField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('subcategory', models.CharField(blank=True, max_length=60, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='DOB')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('profile_photo', models.CharField(blank=True, max_length=300, null=True)),
                ('sex', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True)),
                ('type_of_body', models.CharField(blank=True, choices=[('Slim', 'Slim'), ('Average', 'Average'), ('Athletic', 'Athletic'), ('Heavyset', 'Heavyset')], max_length=8, null=True)),
                ('feet', models.PositiveIntegerField(blank=True, null=True)),
                ('inches', models.PositiveIntegerField(blank=True, null=True)),
                ('lives_in', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('skills', models.ManyToManyField(related_name='skills', to='accounts.Skill')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FollowLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('following', 'following'), ('unfollowed', 'unfollowed'), ('blocked', 'blocked')], default='following', max_length=30)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('unfollowed_on', models.DateTimeField(null=True)),
                ('blocked_on', models.DateTimeField(null=True)),
                ('followed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
