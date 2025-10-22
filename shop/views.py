from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView

from .models import Category, Product

class Index(ListView):
    """Главная старничка"""
    model = Product
    extra_context = {'title':'Главная страница'}
    template_name = 'shop/index.html'