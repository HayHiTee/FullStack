# Generated by Django 2.1.7 on 2019-03-18 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FullStackApp', '0004_auto_20190317_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='tracking_id',
            field=models.CharField(default=0, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='day_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='eve_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mob_phone',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_related_customer', to='FullStackApp.Customer'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='shipping_type',
            field=models.CharField(choices=[('Nxt_day', 'Next Day'), ('std', 'Standard'), ('Free', 'Free')], default='Free', max_length=100),
        ),
    ]