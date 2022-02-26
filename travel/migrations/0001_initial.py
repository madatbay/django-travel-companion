# Generated by Django 4.0.2 on 2022-02-26 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Destination name (City, Country, etc.)', max_length=50)),
                ('description', models.TextField(help_text='Short description for destination')),
                ('image', models.ImageField(help_text='Image to identify destination easily', upload_to='destinations/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='Short trip description', max_length=200)),
                ('start_date', models.DateField(help_text='Trip start date')),
                ('end_date', models.DateField(help_text='Trip end date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('destinations', models.ManyToManyField(blank=True, help_text='Add destinations to your trip', related_name='destinations', to='travel.Destination')),
                ('trip_mates', models.ManyToManyField(blank=True, help_text='Choose who is going with you', related_name='mates', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('address', models.CharField(help_text='Hotel address to locate it easily', max_length=200)),
                ('rate', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, help_text='Hotel rate you will stay')),
                ('checkin_date', models.DateField(help_text='Date when is required to check in')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='travel.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkin_date', models.DateField(help_text='Date when is required to check in')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_loc', models.ForeignKey(help_text='Point the location where you will fly', on_delete=django.db.models.deletion.CASCADE, related_name='from_loc', to='travel.destination')),
                ('to_loc', models.ForeignKey(help_text='Point the destination where to fly', on_delete=django.db.models.deletion.CASCADE, related_name='to_loc', to='travel.destination')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='travel.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Name for the expence', max_length=50)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item_price', models.FloatField(default=0, help_text='Price for item per 1 quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('budget', models.ForeignKey(help_text='Parent budget', on_delete=django.db.models.deletion.CASCADE, to='travel.budget')),
            ],
        ),
        migrations.AddField(
            model_name='budget',
            name='trip',
            field=models.OneToOneField(help_text='Link Budget item to any trip', on_delete=django.db.models.deletion.CASCADE, to='travel.trip'),
        ),
    ]
