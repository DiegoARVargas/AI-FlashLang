# Generated by Django 5.1.7 on 2025-07-04 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='preferred_language',
            field=models.CharField(choices=[('es', 'Español'), ('en', 'Inglés'), ('fr-CA', 'Francés (Canadá)'), ('pt-BR', 'Portugués (Brasil)')], default='es', max_length=10),
        ),
    ]
