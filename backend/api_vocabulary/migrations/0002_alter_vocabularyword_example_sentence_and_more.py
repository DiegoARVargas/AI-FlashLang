# Generated by Django 5.1.7 on 2025-03-26 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_vocabulary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vocabularyword',
            name='example_sentence',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularyword',
            name='example_translation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularyword',
            name='part_of_speech',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='vocabularyword',
            name='translation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
