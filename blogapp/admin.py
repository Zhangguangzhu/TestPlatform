# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import models

from django.contrib import admin

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
	fields = ['release_time','title','content','counter']

admin.site.register(models.Article, ArticleAdmin)