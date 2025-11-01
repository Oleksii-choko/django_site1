from tkinter.constants import CASCADE

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Категория", related_name='subcategory')

    def get_absolute_url(self):
        """Ссылка на категорию"""
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    def get_parent_category_photo(self):  # щоб діставав фото категорій
        if self.image:
            return self.image.url
        else:
            return 'https://placehold.co/600x400/EEEEEE/222222?text=No+Image'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование товара')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания товар')
    watched = models.IntegerField(default=0, verbose_name='Просмотры')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь скоро будет описание...', verbose_name='Описание товара')
    info = models.TextField(default='Дополнительная Информация о продукте', verbose_name='Информация о товаре')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размер в мм')
    color = models.CharField(max_length=30, default='Серебро', verbose_name='Цвет/Материал')

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Товар: pk={self.pk}, title={self.title}, price={self.price}'

    def get_first_photo(self):  # щоб діставав фото категорій
        if self.images.first():
            return self.images.first().image.url
        else:
            return 'https://placehold.co/600x400/EEEEEE/222222?text=No+Image'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея товаров'


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Контактное имя')
    email = models.EmailField(verbose_name='Почта')
    subject = models.CharField(max_length=150, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания сообщения')
    is_processed = models.BooleanField(default=False, verbose_name='Состояние')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Mail(models.Model):
    """Почтовая рассылка"""
    mail = models.EmailField(unique=True, verbose_name='Почта')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почты'
