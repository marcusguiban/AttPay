# Generated by Django 5.0.6 on 2024-06-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_companyid'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='on_duty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='on_duty',
            field=models.BooleanField(default=False),
        ),
    ]