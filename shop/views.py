from itertools import product

from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.views.generic import ListView, DetailView

from .models import Category, Product


class Index(ListView):
    """Главная старничка"""
    model = Product
    context_object_name = 'categories'
    extra_context = {'title': 'Главная страница'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """Вывод родительских категорий"""
        categories = Category.objects.filter(parent=None)
        return categories

    def get_context_data(self, *, object_list=None, **kwargs):  # вывод з бд
        """Вывод на страничку дополнительных элементов"""
        context = super().get_context_data()  # Словарь
        context['top_product'] = Product.objects.order_by('-watched')[:3]
        return context


class SubCategories(ListView):
    """Вывод подкатегории на отдельной страничке"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/shop.html'

    def get_queryset(self):
        """Получение всех товаров определенной категории"""

        if type_fild := self.request.GET.get('type'):
            products = Product.objects.filter(category__slug=type_fild)
            return products

        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategory.all()
        products = Product.objects.filter(category__in=subcategories).order_by('?')

        if sort_field := self.request.GET.get('sort'):
            products = products.order_by(sort_field)
        return products

    def get_context_data(self, *, object_list=None, **kwargs):
        """Дополнительные элементы"""
        context = super().get_context_data()
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context
