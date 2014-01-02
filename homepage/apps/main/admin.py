from django.contrib import admin
from apps.main.models import Question,Answer, Response, Profile, SavedQuestion


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]
	list_display = ('question', 'category', 'points', 'time', 'is_new', 'visible')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Response)
admin.site.register(Profile)
admin.site.register(SavedQuestion)
