# Create your views here.
from django.shortcuts import render, get_object_or_404
from apps.main.models import Question, Answer, Response, Profile, SavedQuestion
from apps.main.models import ResponseForm, QuestionForm, AnswerForm, SavedQForm, ProfileForm
import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Sum, Count
from apps.main.utils import order_by_score
from django.utils import simplejson
from endless_pagination.decorators import page_template
from django.db.models.base import ObjectDoesNotExist

# r = Response.objects.values('answer__answer').annotate(ac=Count('user'))
   # outputs the number of responses for each answer (by id) of each question

# r = Response.objects.filter(answer__question=1).values_list('answer__answer').annotate(ac=Count('user'))
   # outputs the number of responses for each answer (by id) of ONE question


def deletequestion(request):
	questions = Question.objects.filter(user=request.user)

	if request.method=='POST':
		if 'qdelete' in request.POST:
			itemid = request.POST['id']
			Question.objects.get(id=itemid).delete()  ##just make hidden instead
			return HttpResponseRedirect(reverse('apps.main.views.deletequestion', args=()))

	context = {'questions':questions}
	return render(request, 'main/deletequestion.html', context)

def itempage(request, itemid):
	question = Question.objects.get(id=itemid)
	answers = Answer.objects.filter(question=question)
	r = Response.objects.filter(answer__question=question).values_list('answer__answer').annotate(ac=Count('user'))
	response = simplejson.dumps(dict(r))

	context = {'question':question, 'response':response, 'answers':answers}
	return render(request, 'main/itempage.html', context)


def ajaxsave(request):
	if request.method == "POST" and request.is_ajax(): 
		savedqform = SavedQForm(request.POST)
		if savedqform.is_valid():
			instance = savedqform.save(commit=False)
			try: 
				SavedQuestion.objects.get(user=request.user.id, question=instance.question).delete()
			except: 
				instance.user = request.user
				instance.save()

		return HttpResponse('worked!')

def ajaxanswer(request):
	if request.method == "POST" and request.is_ajax(): 
		if request.user.is_authenticated():
			form = ResponseForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				try: Response.objects.get(answer=instance.answer, user=request.user.id).delete()
				except Response.DoesNotExist: 
					q = Question.objects.get(id=instance.answer.question.id)
					q.points = q.points + 1
					q.save()

				instance.user = request.user
				instance.save()

				r = Response.objects.filter(answer__question=instance.answer.question).values_list('answer__answer').annotate(ac=Count('user'))
				response_dict = dict(r)

				return HttpResponse(simplejson.dumps(response_dict))

		return HttpResponse('didnt work!')

@page_template('main/paginate.html')   #part of endless scroll to add pagetemplate to context and help with ajax
def index(request, template = 'main/index.html', extra_context=None):
	questions = Question.objects.filter(visible=True)
	questions = order_by_score(questions, 'points', 'time')

	answers = Answer.objects.all()

	try:  
		r = Response.objects.filter(user=request.user.id)
		responses = [i.answer.question.id for i in r]
	except: responses=[]

	try: 
		s = SavedQuestion.objects.filter(user=request.user.id)
		saved = [i.question.id for i in s]
	except: saved=[]

	form = ResponseForm()
	savedqform = SavedQForm()


	context = {'questions':questions, 'answers':answers, 'form':form, 'responses':responses, 'savedqform':savedqform, 'saved':saved, }
	
	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)


def addquestion(request):
	try: questions = Question.objects.filter(user=request.user).order_by('-time')
	except: questions = []

	form = QuestionForm()

	if request.method=='POST':
		if 'qsubmit' in request.POST:
			form = QuestionForm(request.POST, request.FILES)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				return HttpResponseRedirect(reverse('apps.main.views.addanswer', args=()))	

	context = {'form':form, 'questions':questions}
	return render(request, 'main/addquestion.html', context)

def addanswer(request):
	user=request.user
	form = AnswerForm(user)

	if request.method=='POST':
		if 'qsubmit' in request.POST:
			form = AnswerForm(user,request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				# addedans = str(instance.answer)
				instance.save()
				if Answer.objects.filter(question__id = instance.question.id).count() == 2 :
					q = Question.objects.get(id=instance.question.id)
					q.visible = True
					q.save()
				return HttpResponseRedirect(reverse('apps.main.views.addanswer',))


	context = {'form':form,}
	return render(request, 'main/addanswer.html', context)


@page_template('main/paginate.html')   #part of endless scroll to add pagetemplate to context and help with ajax
def category(request, category, template = 'main/index.html', extra_context=None):
	questions = Question.objects.filter(category__iexact=category.lower(), visible=True)
	questions = order_by_score(questions, 'points', 'time')
	if not questions: raise Http404

	answers = Answer.objects.filter(question__category__iexact=category.lower())

	try: 
		r = Response.objects.filter(user=request.user.id)
		responses = [i.answer.question.id for i in r]
	except: responses=[]

	try: 
		s = SavedQuestion.objects.filter(user=request.user.id)
		saved = [i.question.id for i in s]
	except: saved=[]

	form = ResponseForm()
	savedqform = SavedQForm()


	context = {'questions':questions, 'answers':answers, 'form':form, 'responses':responses, 'savedqform':savedqform, 'saved':saved, 'newtab':True}
	
	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)


@page_template('main/paginate.html')   #part of endless scroll to add pagetemplate to context and help with ajax
def categorynew(request, category, template = 'main/index.html', extra_context=None):
	questions = Question.objects.filter(category__iexact=category.lower(), visible=True).order_by('-time')
	if not questions: raise Http404

	answers = Answer.objects.filter(question__category__iexact=category.lower())

	try: 
		r = Response.objects.filter(user=request.user.id)
		responses = [i.answer.question.id for i in r]
	except: responses=[]

	try: 
		s = SavedQuestion.objects.filter(user=request.user.id)
		saved = [i.question.id for i in s]
	except: saved=[]

	form = ResponseForm()
	savedqform = SavedQForm()


	context = {'questions':questions, 'answers':answers, 'form':form, 'responses':responses, 'savedqform':savedqform, 'saved':saved, }
	
	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)


@page_template('main/paginate.html')   #part of endless scroll to add pagetemplate to context and help with ajax
def saved(request, template = 'main/index.html', extra_context=None):
	try: 
		s = SavedQuestion.objects.filter(user=request.user.id)
		saved = [i.question.id for i in s]
	except: saved=[]

	questions = Question.objects.filter(id__in=saved, visible=True)
	answers = Answer.objects.all()
	try: 
		r = Response.objects.filter(user=request.user.id)
		responses = [i.answer.question.id for i in r]
	except: responses=[]

	form = ResponseForm()
	savedqform = SavedQForm()
 
	if request.method=='POST':
		if 'removesavequestion' in request.POST:
			savedqform = SavedQForm(request.POST)
			if savedqform.is_valid():
				instance = savedqform.save(commit=False)
				SavedQuestion.objects.get(question__id=instance.question.id).delete()

				return HttpResponseRedirect(reverse('apps.main.views.index', args=()))


	context = {'questions':questions, 'answers':answers, 'form':form, 'responses':responses, 'savedqform':savedqform, 'saved':saved}
	
	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

@page_template('main/paginate.html')   #part of endless scroll to add pagetemplate to context and help with ajax
def submitted(request, template = 'main/index.html', extra_context=None):
	questions = Question.objects.filter(user=request.user)
	answers = Answer.objects.filter(question__user=request.user)

	try: 
		r = Response.objects.filter(user=request.user.id)
		responses = [i.answer.question.id for i in r]
	except: responses=[]

	try: 
		s = SavedQuestion.objects.filter(user=request.user.id)
		saved = [i.question.id for i in s]
	except: saved=[]

	form = ResponseForm()
	savedqform = SavedQForm()


	context = {'questions':questions, 'answers':answers, 'form':form, 'responses':responses, 'savedqform':savedqform, 'saved':saved, }
	
	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

def scoreboard(request):
	questions = Question.objects.values('user__username').annotate(sumpts=Sum('points')).order_by('-sumpts')[:100]
	context = {'questions':questions}
	return render(request, 'main/scoreboard.html', context)

def profile(request):
	try: 
		oldprofile = Profile.objects.get(user=request.user)
		form = ProfileForm(instance=oldprofile)

	except ObjectDoesNotExist: 
		form = ProfileForm()

	if request.method=='POST':
		if 'addprofile' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				return HttpResponseRedirect(reverse('apps.main.views.addquestion', args=()))
	context = {'form':form}
	return render(request, 'main/profile.html', context)

def newprofile(request):
	try: 
		oldprofile = Profile.objects.get(user=request.user)
		return HttpResponseRedirect(reverse('apps.main.views.addquestion', args=()))

	except ObjectDoesNotExist: 
		form = ProfileForm()

	if request.method=='POST':
		if 'addprofile' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				return HttpResponseRedirect(reverse('apps.main.views.addquestion', args=()))
	context = {'form':form}
	return render(request, 'main/profile.html', context)