# Generated by Django 4.2.10 on 2024-06-01 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_promocode'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes/'),
        ),
    ]
