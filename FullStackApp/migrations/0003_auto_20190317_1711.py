# Generated by Django 2.1.7 on 2019-03-17 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FullStackApp', '0002_auto_20190317_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='', max_length=500, null=True),
        ),
    ]