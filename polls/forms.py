from django import forms 


class NewPoll(forms.Form):
	question = forms.CharField(max_length=100)
	choice_1 = forms.CharField(max_length=100)
	choice_2 = forms.CharField(max_length=100)
	choice_3 = forms.CharField(max_length=100)
	choice_4 = forms.CharField(max_length=100)
