# Generated by Django 5.0 on 2024-03-18 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0007_article_xml'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='submission_link',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
