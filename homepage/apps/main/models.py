from django.db import models
from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import StrictButton
from django.core.exceptions import ValidationError
import StringIO
from PIL import Image
from django.utils import timezone
import datetime
from mezzanine.generic.fields import RatingField, CommentsField
from mezzanine.core.models import Displayable, Ownable
from django.core.files.storage import default_storage as storage

class Profile(models.Model):
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'), 
		)
	user = models.OneToOneField("auth.User")
	age = models.IntegerField(max_length=2)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
	zipcode = models.IntegerField(max_length=5)
	state = models.CharField(max_length=15)

	def __unicode__(self):
		return "%s" % (self.user)


class Question(models.Model):
	question = models.CharField(max_length=140)
	picture = models.ImageField(upload_to='questions', null=True, blank=True)
	time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User)
	category = models.CharField(max_length=100)
	points = models.IntegerField(default=1)  #default to 1
	comments = CommentsField()
	description = models.TextField()
	visible = models.BooleanField()

	def is_new(self):
		return self.time >= timezone.now() - datetime.timedelta(minutes=10)

	def get_absolute_url(self):
		from django.core.urlresolvers import reverse
		return reverse('apps.main.views.itempage', args=[str(self.id)])

	# def save(self, size=(500, 300)):
	# 	"""
	# 	Save Photo after ensuring it is not blank.  Resize as needed.
	# 	"""
	# 	if not self.picture and not self.id:
	# 		return

	# 	super(Question, self).save()
	# 	filename = str(self.picture.url)
	# 	image = Image.open(self.picture)
	# 	image.thumbnail(size, Image.ANTIALIAS)
	# 	fh = storage.open(self.picture.name, "w")
	# 	format = 'jpeg'  # You need to set the correct image format here
	# 	image.save(fh, format)
	# 	fh.close()
		# image.save(filename)

	def __unicode__(self):
		return self.question

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=30)  #make higher to 50

	def __unicode__(self):
		return "%s (%s)" % (self.answer, self.question)

class Response(models.Model):
	answer = models.ForeignKey(Answer)
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return "%s - %s (%s)" % (self.answer.answer, self.answer.question, self.user)


class SavedQuestion(models.Model):
	question = models.ForeignKey(Question)
	user = models.ForeignKey(User)
	time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.question.question

# ##########    FORMS   ############

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		exclude = ['user']

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.helper= FormHelper()
		self.helper.layout = Layout(
				'age' ,
				'gender' ,
				'zipcode' ,
				'state',
		    StrictButton('Submit', name='addprofile', type='submit',css_class='btn-primary'),
		)

class ResponseForm(ModelForm):
	class Meta:
		model = Response
		exclude = ['user', 'time']

class SavedQForm(ModelForm):
	class Meta:
		model = SavedQuestion
		exclude = ['user', 'time']

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		exclude = ['time', 'user', 'points']

	def __init__(self, *args, **kwargs):
		super(QuestionForm, self).__init__(*args, **kwargs)
		self.helper= FormHelper()
		self.helper.layout = Layout(
				'question' ,
				'category' ,
				'picture' ,
				'description',
		    StrictButton('Submit', name='qsubmit', type='submit',css_class='btn-primary'),
		)
 
	def clean(self):
		cleaned_data = super(QuestionForm, self).clean()
		image= cleaned_data.get('picture',False)

		if image:
			if image._size > 2*1024*1024:
				raise ValidationError("Image file too large ( > 2.0mb )")

	# 		pilimage = Image.open(image) 
	# 		if pilimage.size[0] < 175 or pilimage.size[1] < 100: #image.size is a 2-tuple (width, height)
	# 			raise ValidationError("Image is too small")

			# pilimage.thumbnail((500,900), Image.ANTIALIAS)
			# pilimage.save(outfile, "JPEG")

		# else:
		# 	raise ValidationError("Couldn't read uploaded image")

		return cleaned_data



class AnswerForm(ModelForm):
	class Meta:
		model = Answer
		exclude = ['user']

	def __init__(self, user, *args, **kwargs):
		super(AnswerForm, self).__init__(*args, **kwargs)
		tenmin = datetime.datetime.now() - datetime.timedelta(minutes=10)
		self.fields['question'].queryset = Question.objects.filter(user=user.id, time__gte=tenmin)
		self.helper= FormHelper()
		self.helper.layout = Layout(
				'question' ,
				'answer' ,
		    StrictButton('Submit', name='qsubmit', type='submit',css_class='btn-primary'),
		)
 
	def clean(self):
		cleaned_data = super(AnswerForm, self).clean()
		question_object= cleaned_data.get('question')

		if not Question.objects.get(id=question_object.id).is_new():
			raise forms.ValidationError('Question too old to add answers!')
		if Answer.objects.filter(question= question_object).count() > 6:
			raise forms.ValidationError('Only 7 answers allowed!')

		return cleaned_data

