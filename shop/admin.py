from django.contrib import admin
from .models import Product, Category, Gallery, ContactMessage
from django.utils.safestring import mark_safe  # для отображение изображения в хтмл тега


class GalleryInline(admin.TabularInline):
    fk_name ='product'
    model = Gallery
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):  #вывести з бд количество предметов по категории
        if obj.products:
            return str(len(obj.products.all())) #обязательно в строковом представление для админки
        else:
            return '0'

    get_products_count.short_description ='Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'color', 'get_photo')
    list_editable = ('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links = ('title', 'pk')
    inlines = (GalleryInline, )

    def get_photo(self, obj):   # для отображение миниатюры
        if obj.images.all():
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)

admin.site.register(Gallery)
