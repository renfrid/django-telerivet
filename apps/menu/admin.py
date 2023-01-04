from django.contrib import admin
from .models import *

# Register your models here.
class SubMenuInline(admin.TabularInline):
    model = SubMenu
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['sequence', 'step', 'keyword', 'title', 'flag']
    search_fields = ['title__startwith']
    ordering = ("sequence",)
    inlines  = [SubMenuInline]


@admin.register(MenuLink)
class MenuLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu', 'sub_menu', 'link']
    ordering = ("id",)

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ["title"]