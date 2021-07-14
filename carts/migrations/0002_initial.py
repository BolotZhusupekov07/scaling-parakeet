# Generated by Django 3.2.4 on 2021-07-08 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemcheckout',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variation'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.variation'),
        ),
        migrations.AddField(
            model_name='cartcheckout',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart'),
        ),
        migrations.AddField(
            model_name='cartcheckout',
            name='products',
            field=models.ManyToManyField(to='carts.CartItemCheckout'),
        ),
    ]