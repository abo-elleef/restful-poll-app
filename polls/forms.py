from django import forms 
from polls.models import Poll,Choice



class NewPoll(forms.Form):
	question = forms.CharField(max_length=100)
	choice_1 = forms.CharField(max_length=100)
	choice_2 = forms.CharField(max_length=100)
	choice_3 = forms.CharField(max_length=100)
	choice_4 = forms.CharField(max_length=100)
class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
    	exclude = ('pub_date',)
    
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
    	exclude = ('poll',)