# Generated by Django 4.2.4 on 2023-10-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vecindad', '0007_mensaje_solicitud_espacios'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='fecha_solicitud',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
