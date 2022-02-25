# Generated by Django 4.0.2 on 2022-02-24 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0002_alter_trip_trip_mates'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('trip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='travel.trip')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('item_price', models.PositiveIntegerField(default=0, help_text='Price for item per 1 quantity')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='travel.budget')),
            ],
        ),
    ]