from django import template
from shop.models import Category, FavouriteProducts

register = template.Library()


@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)


@register.simple_tag()
def get_sorted():
    sorters = [
        {
            'title': 'Цена',
            'sorters': [
                ('price', 'по возрастанию'),
                ('-price', 'по убыванию')

            ]
        },
        {
            'title': 'Цвет',
            'sorters': [
                ('color', 'от А до Я'),
                ('-color', 'от Я до А')

            ]
        },
        {
            'title': 'Размер',
            'sorters': [
                ('size', 'по возрастанию'),
                ('-size', 'по убыванию')

            ]
        }
    ]
    return sorters

@register.simple_tag()
def get_favourite_products(user):
    """Вывод избранных товаров на страничку"""
    fav = FavouriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products