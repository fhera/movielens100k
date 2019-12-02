# Generated by Django 2.2.7 on 2019-11-30 14:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puntuacion',
            name='puntuacion',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Mala'), (5, 'Muy buena'), (1, 'Muy mala'), (4, 'Buena'), (3, 'Regular')], validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Puntuación'),
        ),
    ]
