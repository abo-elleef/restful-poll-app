# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from polls.models import Poll,Choice
from polls.forms import NewPoll
from django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse

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

		else:
			raise Exception("I know python!")
		return HttpResponseRedirect(reverse('polls:index'))
	else:
		context = {'form':NewPoll()}
		return render(request,'polls/new.html',context)

def edit(request,poll_id):
	poll = get_object_or_404(poll,pk=poll_id)
	context = {'poll':poll}
	return render(request,'polls/edit.html',context)

def update(request,poll_id):
	poll = get_object_or_404(Poll, pk= poll_id)
	try:
		choice = poll.choice_set.get(pk=request.POST['choice'])
	except KeyError, Choice.DoesNotExist:
		context = {'error_message':"You didn't select any choices",'poll':poll}
		return render(request,'polls/show.html',context)
	else:
		choice.votes += 1
		choice.save()
		return HttpResponseRedirect(reverse('polls:index'))

def destroy(request,poll_id):
	poll = get_object_or_404(Poll,pk=poll_id)
	poll.delete()	
	return HttpResponseRedirect(reverse('polls:index'))
	