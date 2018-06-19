# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class Article(models.Model):

		title = models.CharField(max_length=32, default="title", primary_key=True)
		content = models.TextField(null=True)
		release_time = models.DateTimeField('发布时间',default=timezone.now)
		last_edit_time = models.DateTimeField('最后修改', auto_now=True)
		counter = models.IntegerField(default=0)
		author = models.CharField(max_length=32, null=True)

		def __unicode__(self):
			return self.title
