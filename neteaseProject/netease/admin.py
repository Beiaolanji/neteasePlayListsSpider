from django.contrib import admin
from .models import *


# Register your models here.
class SingerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)  # 展示字段
    list_per_page = 10  # 分页 每页显示的条数
    ordering = ('id',)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)  # 展示字段
    list_per_page = 10  # 分页 每页显示的条数
    ordering = ('id',)


class PlayListAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'url')
    list_display = ('id', 'name', 'url', 'time', 'singer', 'album')  # 展示字段
    list_per_page = 10  # 分页 每页显示的条数
    ordering = ('id',)


admin.site.register(Singer, SingerAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(PlayList, PlayListAdmin)
