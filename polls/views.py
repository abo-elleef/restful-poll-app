# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from polls.models import Poll,Choice
from polls.forms import NewPoll,PollForm,ChoiceForm
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

def index(request):
	polls = Poll.objects.order_by('-pub_date')
	context ={'polls':polls} 
	return render(request,'polls/index.html',context)

def show(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	context={"poll":poll}
	return render(request,'polls/show.html',context)

def new(request):
	poll = NewPoll()   #Poll.new()
	context ={'poll':poll}
	return render(request,'polls/new.html',context)

def create(request):
	if request.method == 'POST':
		form = NewPoll(request.POST)
		if form.is_valid():
			clean_inputs_and_create(form)
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		context = {'form':NewPoll()}
		return render(request,'polls/new.html',context)

def vote(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	context = {'poll':poll}
	return render(request,'polls/vote.html',context)

def add_vote(request,poll_id):
	poll = get_object_or_404(Poll, pk= poll_id)
	try:
		choice = poll.choice_set.get(pk=request.POST['choice'])
	except KeyError, Choice.DoesNotExist:
		context = {'error_message':"You didn't select any choices",'poll':poll}
		return render(request,'polls/vote.html',context)
	else:
		choice.votes += 1
		choice.save()
		return HttpResponseRedirect(reverse('polls:index'))

def destroy(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	poll.delete()	
	return HttpResponseRedirect(reverse('polls:index'))


def edit(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	poll_form = PollForm(instance=poll)
	choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',))
	form_set = choices_form_set(queryset = Choice.objects.filter(poll_id = poll.id))
	context = {'poll_form':poll_form,'poll':poll,'choices':form_set}
	return render(request,'polls/edit.html',context)

def update(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	if request.method == "POST":
		form = PollForm(request.POST,instance=poll)
		if form.is_valid():
			form.save()
		print "going"
		choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',))
		print "going"
		form_set =choices_form_set(request.POST)
		if form_set.is_valid():
			form_set.save()
		print "going"
		# if form.is_valid:
		# 	clean_inputs_and_update(form,poll)
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		context = {'form':NewPoll(poll)}
		return render(request,'polls/edit.html',context)

			

def clean_inputs_and_create(form):
	question = form.cleaned_data['question']
	choice_1 = form.cleaned_data['choice_1']
	choice_2 = form.cleaned_data['choice_2']
	choice_3 = form.cleaned_data['choice_3']
	choice_4 = form.cleaned_data['choice_4']
	poll = Poll(question=question)
	poll.save()
	choices = [choice_1,choice_2,choice_3,choice_4]
	for choice in choices:
		choice = Choice(choice_text = choice, poll_id = poll.id)
		choice.save()
def clean_inputs_and_update(form,poll):
	question = form.cleaned_data['question']
	choice_1 = form.cleaned_data['choice_1']
	choice_2 = form.cleaned_data['choice_2']
	choice_3 = form.cleaned_data['choice_3']
	choice_4 = form.cleaned_data['choice_4']
	poll.question = question
	poll.save()
	new_choices = [choice_1,choice_2,choice_3,choice_4]
	choices = poll.choice_set
	for i in range(0,4):
		choices[i].choice_text = new_choices[i]
		choices[i].save()