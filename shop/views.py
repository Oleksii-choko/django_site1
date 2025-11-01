from itertools import product
from symtable import Class

import django.db.utils
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.utils import IntegrityError

from .models import Category, Product, ContactMessage, FavouriteProducts, Mail
from .forms import LoginForm, RegistrationForm, ContactForm


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


def about_us(request):
    """Страница про нас"""
    context = {
        'title': 'Про нас'
    }
    return render(request, 'shop/about.html', context)


def contact_us(request):
    """Страница про нас"""
    context = {
        'title': 'Контакти'
    }
    return render(request, 'shop/contact.html', context)


class ProductPage(DetailView):
    """Вывод товара на отдельной странице"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/shop-single.html'

    def get_context_data(self, **kwargs):
        """Вывод дополнительных элементов"""
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['title'] = product.title
        # products = Product.objects.filter(category=product.category)
        products = Product.objects.all().exclude(slug=self.kwargs['slug']).filter(category=product.category)[:5]
        context['products'] = products
        return context


def login_regіstration(request):
    context = {"title": 'Войти или зарегистрироваться',
               'login_form': LoginForm,
               'registration_form': RegistrationForm}

    return render(request, 'shop/login_registration.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Не верное Имя пользователя или Пароль')
        return redirect('login_registration')


def user_logout(request):
    logout(request)
    return redirect('index')


def user_registration(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Аккаунт пользователя создан успешно!')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
        # messages.error(request, 'Что-то пошло не так')
    return redirect('login_registration')


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Спасибо! Сообщение отправлено.')
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'shop/contact.html', {'form': form, 'title': 'Контакты'})


def save_favourite_product(request, product_slug):
    """Добавление или удаление товара из избранных"""
    next_page = request.META.get('HTTP_REFERER', 'index')
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(slug=product_slug)
        favourite_products = FavouriteProducts.objects.filter(user=user)

        if product in [i.product for i in favourite_products]:
            fav_product = FavouriteProducts.objects.get(user=user, product=product)
            fav_product.delete()
        else:
            FavouriteProducts.objects.create(user=user, product=product)

        next_page = request.META.get('HTTP_REFERER', 'index')
    return redirect(next_page)


class FavoriteProductsView(LoginRequiredMixin, ListView):
    """Для Вывода избранных на страничку"""
    model = FavouriteProducts
    context_object_name = 'products'
    template_name = 'shop/favorite_products.html'
    login_url = 'user_registration'

    def get_queryset(self):
        """Получаем товары конкретного пользователя"""
        favs = FavouriteProducts.objects.filter(user=self.request.user)
        products = [i.product for i in favs]
        return products


def save_subscribers(request):
    """СОбрать почтовых адресов"""
    email = request.POST.get('email')
    user = request.user if request.user.is_authenticated else None
    if email:
        try:
            Mail.objects.create(mail=email, user=user)
        except IntegrityError:
            messages.error(request, 'Вы уже являетесь подписчиком')

    return redirect('index')


def send_email_to_subscribers(request):
    """Отправка писем пользователям"""
    from conf import settings
    from django.core.mail import send_mail
    if request.method == 'POST':
        text = request.POST.get('text')
        mail_lists = Mail.objects.all()
        for email in mail_lists:
            send_mail(
                subject="У нас новая акция",
                message=text,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
    context = {'title':'Спамер'}
    return render(request,'shop/_send_email.html', context)
