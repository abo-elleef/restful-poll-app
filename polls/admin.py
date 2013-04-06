from django.contrib import admin
from polls.models import Poll
from polls.models import Choice


class ChoiceInline(admin.StackedInline):
	model = Choice 
	extra = 2

class PollAdmin(admin.ModelAdmin):
	fields = ['question', 'pub_date']
	inlines=[ChoiceInline]
	list_display = ('question','pub_date','was_published_recently')


admin.site.register(Poll,PollAdmin)