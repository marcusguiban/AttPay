# Generated by Django 5.0.6 on 2024-06-30 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_payslip_duration_remove_schedule_friday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='on_duty',
            field=models.BooleanField(default=False),
        ),
    ]
