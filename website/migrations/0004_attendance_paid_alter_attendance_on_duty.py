# Generated by Django 5.0.6 on 2024-06-30 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_attendance_on_duty'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='on_duty',
            field=models.BooleanField(default=True),
        ),
    ]
