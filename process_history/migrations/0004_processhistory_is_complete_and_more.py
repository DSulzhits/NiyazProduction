# Generated by Django 5.0.9 on 2024-11-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process_history', '0003_processhistory_assignment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='processhistory',
            name='is_complete',
            field=models.BooleanField(default=False, verbose_name='Отметка о выполнении задания'),
        ),
        migrations.DeleteModel(
            name='CompleteProcessHistoryView',
        ),
    ]
