# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Article(models.Model):

		title = models.CharField(max_length=32, default="title", primary_key=True)
		content = models.TextField(null=True)
		release_time = models.DateTimeField('release time')
		counter = models.IntegerField(default=0)

		def __unicode__(self):
			return self.title
