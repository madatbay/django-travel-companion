# Generated by Django 4.0.2 on 2022-02-24 18:31

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
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(help_text='Short trip description', max_length=200)),
                ('start_date', models.DateField(help_text='Trip start date')),
                ('end_date', models.DateField(help_text='Trip end date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trip_mates', models.ManyToManyField(help_text='Choose who is going with you', related_name='mates', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]