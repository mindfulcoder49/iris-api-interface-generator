# Generated by Django 5.1.1 on 2024-09-22 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiquery', '0002_apiquerytemplate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiquery',
            name='query',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='apiquerytemplate',
            name='form_fields',
            field=models.JSONField(),
        ),
    ]
