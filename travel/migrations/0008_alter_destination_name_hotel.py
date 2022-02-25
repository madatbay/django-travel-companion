# Generated by Django 4.0.2 on 2022-02-25 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0007_alter_budget_trip_alter_budgetitem_budget_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='name',
            field=models.CharField(help_text='Destination name (City, Country, etc.)', max_length=50),
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
    ]