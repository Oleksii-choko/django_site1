from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView

from .models import Category, Product

class Index(ListView):
    """Главная старничка"""
    model = Product
    context_object_name = 'categories'
    extra_context = {'title':'Главная страница'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """Вывод родительских категорий"""
        categories = Category.objects.filter(parent=None)
        return categories


class SubCategories(ListView):
    """Вывод подкатегории на отдельной страничке"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/shop.html'

    def get_queryset(self):
        """Получение всех товаров определенной категории"""
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategory.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')
        return products


