# Generated by Django 5.0.7 on 2024-10-03 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0014_alter_idea_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='last_plan_generated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
