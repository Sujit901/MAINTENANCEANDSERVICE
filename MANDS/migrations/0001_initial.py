# Generated by Django 4.1.5 on 2023-07-04 09:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=400)),
                ('number', models.CharField(max_length=10)),
                ('firstname', models.CharField(max_length=100)),
                ('middlename', models.CharField(blank=True, max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=1000)),
                ('book_date', models.DateField(auto_now=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('price', models.IntegerField()),
                ('service_charge', models.IntegerField()),
                ('parts_name', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('COMPLETED', 'Completed')], default='PENDING', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=1000)),
                ('available', models.CharField(choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable')], default='AVAILABLE', max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=400, unique=True)),
                ('image', models.ImageField(default='/static/profile.png', upload_to='')),
                ('number', models.CharField(max_length=10, unique=True)),
                ('firstname', models.CharField(max_length=100)),
                ('middlename', models.CharField(blank=True, max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=1000)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_token', models.CharField(max_length=100)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('image', models.ImageField(upload_to='')),
                ('product_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=1000)),
                ('available', models.CharField(choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable')], default='AVAILABLE', max_length=11)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MANDS.service')),
            ],
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('image', models.ImageField(upload_to='')),
                ('parts_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=1000)),
                ('available', models.CharField(choices=[('AVAILABLE', 'Available'), ('UNAVAILABLE', 'Unavailable')], default='AVAILABLE', max_length=11)),
                ('price', models.IntegerField()),
                ('service_charge', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MANDS.product')),
            ],
        ),
    ]
