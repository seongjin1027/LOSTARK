# Generated by Django 5.2.3 on 2025-07-09 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='nickname',
            field=models.CharField(default='unknown', max_length=100),
            preserve_default=False,
        ),
    ]
