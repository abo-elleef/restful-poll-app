from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Poll(models.Model):
	question = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('publishing_date',default=datetime.datetime.now())
	
	def __unicode__(self):
		return self.question 

	def was_published_recently(self):
		return self.pub_date >= timezone.now() -  datetime.timedelta(days=1)
	was_published_recently.short_description = "yah recent published"
	was_published_recently.boolean = True
class Choice(models.Model):
	poll = models.ForeignKey(Poll)	
	choice_text = models.CharField(max_length = 200)
	votes = models.IntegerField(default = 0)
	def __unicode__(self):
		return self.choice_text
