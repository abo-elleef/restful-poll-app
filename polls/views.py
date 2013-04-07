# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from polls.models import Poll,Choice
from polls.forms import NewPoll,PollForm,ChoiceForm
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory

def index(request ,template = 'polls/index.html'):
	polls = Poll.objects.order_by('-pub_date')
	context ={'polls':polls} 
	return render(request,template,context)

def show(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	context={"poll":poll}
	return render(request,'polls/show.html',context)

def new(request,template = 'polls/new.html'):
	poll = PollForm() 
	choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',),extra=2)
	form_set = choices_form_set(queryset = Choice.objects.none())
	context ={'poll':poll,'choices':form_set}
	return render(request,template,context)

def create(request):
	if request.method == 'POST':
		form = PollForm(request.POST)
		choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',))
		form_set =choices_form_set(request.POST)
		if form.is_valid() and form_set.is_valid:
			poll = form.save()
			choices = form_set.save(commit=False)
			for choice in choices:
				choice.poll_id = poll.id
				choice.save()
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		context = {'form':NewPoll()}
		return render(request,'polls/new.html',context)

def edit(request,poll_id,template = 'polls/edit.html'):
	poll = get_object_or_404(Poll,pk=poll_id)
	poll_form = PollForm(instance=poll)
	choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',))
	form_set = choices_form_set(queryset = Choice.objects.filter(poll_id = poll.id))
	context = {'poll_form':poll_form,'poll':poll,'choices':form_set}
	return render(request,template,context)

def update(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	if request.method == "POST":
		form = PollForm(request.POST,instance=poll)
		choices_form_set = modelformset_factory(Choice,fields=('choice_text','votes',))
		form_set =choices_form_set(request.POST)
		if form.is_valid() and form_set.is_valid:
			form.save()
			form_set.save()
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		context = {'form':NewPoll(poll)}
		return render(request,'polls/edit.html',context)

def destroy(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	poll.delete()	
	return HttpResponseRedirect(reverse('polls:index'))

def vote(request,poll_id,template ='polls/vote.html'):
	poll = get_object_or_404(Poll,pk=poll_id)
	context = {'poll':poll}
	return render(request,template,context)

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



