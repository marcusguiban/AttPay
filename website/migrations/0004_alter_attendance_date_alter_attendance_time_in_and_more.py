# Generated by Django 5.0.6 on 2024-06-01 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_employee_remove_attendance_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time_in',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time_out',
            field=models.TimeField(auto_now=True),
        ),
    ]
