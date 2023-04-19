# Generated by Django 3.2.13 on 2023-04-19 12:45

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=20)),
                ('address_line1', models.CharField(blank=True, max_length=80, null=True)),
                ('address_line2', models.CharField(blank=True, max_length=80, null=True)),
                ('city', models.CharField(max_length=40)),
                ('county', models.CharField(blank=True, max_length=80, null=True)),
                ('postcode', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('delivery_cost', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('grand_total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cart_instance', models.TextField(default='')),
                ('payment_id', models.CharField(default='', max_length=254)),
                ('has_artwork', models.BooleanField(blank=True, default=False, null=True)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='accounts.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('lineitem_total', models.DecimalField(decimal_places=2, editable=False, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineitems', to='checkout.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
