# Generated by Django 5.0.6 on 2024-06-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_attendance_working_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time_in',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='time_out',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='working_hours',
            field=models.CharField(default='0 hours 0 minutes', max_length=50),
        ),
    ]
