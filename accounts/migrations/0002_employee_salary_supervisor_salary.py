# Generated by Django 5.0.6 on 2024-07-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=450, max_digits=10),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=450, max_digits=10),
        ),
    ]
