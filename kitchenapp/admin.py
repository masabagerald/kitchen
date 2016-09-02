from django.contrib import admin

# Register your models here.
from kitchenapp.models import Category, Food,UserProfile


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Food)
admin.site.register(UserProfile)


