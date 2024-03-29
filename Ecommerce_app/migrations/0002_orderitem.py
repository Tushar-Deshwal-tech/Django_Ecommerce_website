# Generated by Django 5.0.2 on 2024-03-12 07:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ecommerce_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_quantity', models.PositiveIntegerField()),
                ('item_size', models.CharField(max_length=10)),
                ('item_color', models.CharField(max_length=20)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Ecommerce_app.orderdata')),
            ],
        ),
    ]
