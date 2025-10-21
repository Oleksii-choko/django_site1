from django.contrib import admin

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title')}

admin.site.register(Product)
admin.site.register(Gallery)
