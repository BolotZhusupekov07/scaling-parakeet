from carts.models import Cart, CartItem
from django.contrib import admin


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]

    class Meta:
        model = Cart


admin.site.register(Cart, CartAdmin)
