from django.contrib import admin
from .models import Product, Order, OrderItem, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') 
    prepopulated_fields = {'slug': ('name',)}  
    search_fields = ('name',)  

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'stock', 'category')  
    prepopulated_fields = {'slug': ('name',)}  
    list_filter = ('category',)      
    search_fields = ('name',) 

class OrderItemInline(admin.TabularInline):
    model = OrderItem  
    extra = 1  

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'is_paid')  
    list_filter = ('is_paid',)  
    inlines = [OrderItemInline]  

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)  
