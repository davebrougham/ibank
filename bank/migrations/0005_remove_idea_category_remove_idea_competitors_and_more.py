# Generated by Django 5.0.7 on 2024-09-18 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_alter_idea_options_idea_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='category',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='competitors',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='complexity',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='downside',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='effort',
        ),
        migrations.RemoveField(
            model_name='idea',
            name='upside',
        ),
    ]
