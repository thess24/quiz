from django.conf import settings
from apps.main.models import Question
from django.db.models import Sum





def score(request): 
	try:
		questions = Question.objects.filter(user=request.user)
		userscore = questions.aggregate(Sum('points'))['points__sum']
		return {'userscore':userscore}

	except: 
		return {}
