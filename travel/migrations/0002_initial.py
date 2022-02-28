# Generated by Django 4.0.2 on 2022-02-28 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trip_mates',
            field=models.ManyToManyField(blank=True, help_text='Choose who is going with you', related_name='mates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='trip',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='travel.destination'),
        ),
        migrations.AddField(
            model_name='flight',
            name='from_loc',
            field=models.ForeignKey(help_text='Point the location where you will fly', on_delete=django.db.models.deletion.CASCADE, related_name='from_loc', to='travel.destination'),
        ),
        migrations.AddField(
            model_name='flight',
            name='to_loc',
            field=models.ForeignKey(help_text='Point the destination where to fly', on_delete=django.db.models.deletion.CASCADE, related_name='to_loc', to='travel.destination'),
        ),
        migrations.AddField(
            model_name='flight',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='travel.trip'),
        ),
        migrations.AddField(
            model_name='flight',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='destination',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='budgetitem',
            name='budget',
            field=models.ForeignKey(help_text='Parent budget', on_delete=django.db.models.deletion.CASCADE, to='travel.budget'),
        ),
        migrations.AddField(
            model_name='budget',
            name='trip',
            field=models.OneToOneField(help_text='Link Budget item to any trip', on_delete=django.db.models.deletion.CASCADE, to='travel.trip'),
        ),
    ]
