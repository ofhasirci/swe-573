# Generated by Django 3.2.4 on 2021-06-22 01:08

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_cleanarticle_topicclass'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=512)),
            ],
        ),
        migrations.AddField(
            model_name='cleanarticle',
            name='ClassValue',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='cleanarticle',
            name='Tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=750), null=True, size=None),
        ),
    ]
